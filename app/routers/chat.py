"""
ESTO ES UN ARCHIVO TEMPORAL

Por mientras se está simulando el "chat" en una vista. La idea es que cuando
se integre la API de WhatsApp se modifique/borre este archivo para que tome los
mensajes reales, no los de la vista.
"""

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.services.contact_service import get_contact_by_id
from app.services.message_service import get_todays_messages, create_message
from app.services.topic_service import get_topics_by_contact
from app.services.gemini_service import get_chat_response

router = APIRouter(prefix="/contacts", tags=["chat"])
templates = Jinja2Templates(directory="app/templates")

# Esta vista se debería borrar una vez que se integre la API de WhatsApp
@router.get("/{contact_id}/chat", response_class=HTMLResponse)
def get_chat_page(
    request: Request, 
    contact_id: int, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    if not current_user or not get_contact_by_id(db, contact_id, current_user.id):
        return RedirectResponse(url="/dashboard", status_code=303)

    contact = get_contact_by_id(db, contact_id, current_user.id)
    messages = get_todays_messages(db, contact_id)

    return templates.TemplateResponse(
        request=request,
        name="chat/index.html",
        context={"request": request, "contact": contact, "messages": messages}
    )

@router.post("/{contact_id}/chat", response_class=HTMLResponse)
def send_chat_message(
    contact_id: int,
    message: str = Form(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user or not get_contact_by_id(db, contact_id, current_user.id):
        return RedirectResponse(url="/dashboard", status_code=303)

    previous_messages = get_todays_messages(db, contact_id)
    chat_history = [{"role": m.role, "content": m.content} for m in previous_messages]

    # con whatsapp deberíamos seguir guardando el mensaje en la base de datos.
    create_message(db, contact_id, role="user", content=message)

    topics_models = get_topics_by_contact(db, contact_id)
    topics_instructions = []
    for topic in topics_models:
        topics_instructions.append(topic.instruction)

    ai_answer = get_chat_response(message, chat_history, topics_instructions)

    # con whatsapp esto también se tiene que guardar de la misma manera
    create_message(db, contact_id, role="model", content=ai_answer)

    return RedirectResponse(url=f"/contacts/{contact_id}/chat", status_code=303)
