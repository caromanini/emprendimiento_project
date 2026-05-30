"""
ESTO ES UN ARCHIVO TEMPORAL

Por mientras se está simulando el "chat" en una vista. La idea es que cuando
se integre la API de WhatsApp se modifique/borre el tab del simulador para que
tome los mensajes reales. El tab de historial WhatsApp ya está listo.
"""

from datetime import date, timedelta
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.services.contact_service import get_contact_by_id
from app.services.message_service import (
    get_todays_messages, get_latest_messages, has_messages_before, create_message
)
from app.services.topic_service import get_topics_by_contact
from app.services.gemini_service import get_chat_response

router = APIRouter(prefix="/contacts", tags=["chat"])
templates = Jinja2Templates(directory="app/templates")


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

    # Tab 1: últimos 20 mensajes reales de WhatsApp
    wa_messages = get_latest_messages(db, contact_id, limit=20, source='whatsapp')
    wa_oldest_id = wa_messages[0].id if wa_messages else None
    wa_has_more = has_messages_before(db, contact_id, wa_oldest_id, source='whatsapp') if wa_oldest_id else False

    # Tab 2: mensajes del simulador del día de hoy
    sim_messages = get_todays_messages(db, contact_id, source='simulator')

    today = date.today()
    yesterday = today - timedelta(days=1)

    return templates.TemplateResponse(
        request=request,
        name="chat/index.html",
        context={
            "request": request,
            "contact": contact,
            "wa_messages": wa_messages,
            "wa_oldest_id": wa_oldest_id,
            "wa_has_more": wa_has_more,
            "sim_messages": sim_messages,
            "today": today.strftime("%Y-%m-%d"),
            "yesterday": yesterday.strftime("%Y-%m-%d"),
        }
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

    previous_messages = get_todays_messages(db, contact_id, source='simulator')
    chat_history = [{"role": m.role, "content": m.content} for m in previous_messages]

    create_message(db, contact_id, role="user", content=message, source='simulator')

    topics_models = get_topics_by_contact(db, contact_id)
    topics_instructions = [t.instruction for t in topics_models]

    ai_answer = get_chat_response(message, chat_history, topics_instructions)

    create_message(db, contact_id, role="model", content=ai_answer, source='simulator')

    # Redirige de vuelta al tab del simulador
    return RedirectResponse(url=f"/contacts/{contact_id}/chat?tab=simulator", status_code=303)
