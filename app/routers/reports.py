from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.services.contact_service import get_contact_by_id
from app.services.message_service import get_todays_messages
from app.services.topic_service import get_topics_by_contact
from app.services.gemini_service import generate_daily_report

router = APIRouter(prefix="/contacts", tags=["reports"])
templates = Jinja2Templates(directory="app/templates")

# modificar esto para que cuando se intente obtener el reporte no se haga un 
# request a la API de Gemini siempre. Si es que ya se realizó el reporte, 
# guardarlo en la base de datos. Para tener un historial y para ahorrar requests
@router.get("/{contact_id}/report", response_class=HTMLResponse)
def get_daily_report_page(
    request: Request, 
    contact_id: int, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    if not current_user or not get_contact_by_id(db, contact_id, current_user.id):
        return RedirectResponse(url="/dashboard", status_code=303)

    contact = get_contact_by_id(db, contact_id, current_user.id)
    todays_messages = get_todays_messages(db, contact_id)

    topics = get_topics_by_contact(db, contact_id)
    
    daily_report_text = "Hoy no se registró comunicación con C.A.M.I"
    if todays_messages:
        daily_report_text = generate_daily_report(todays_messages, topics)

    return templates.TemplateResponse(
        request=request,
        name="reports/daily.html",
        context={"request": request, "contact": contact, "daily_report_text": daily_report_text}
    )