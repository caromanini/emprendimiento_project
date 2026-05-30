from datetime import date, timedelta
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.services.contact_service import get_contact_by_id
from app.services.message_service import get_latest_messages, get_messages_before, has_messages_before

router = APIRouter(prefix="/contacts", tags=["history"])
templates = Jinja2Templates(directory="app/templates")

MESSAGES_PER_PAGE = 20


@router.get("/{contact_id}/history", response_class=HTMLResponse)
def get_history_page(
    request: Request,
    contact_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user or not get_contact_by_id(db, contact_id, current_user.id):
        return RedirectResponse(url="/dashboard", status_code=303)

    contact = get_contact_by_id(db, contact_id, current_user.id)
    messages = get_latest_messages(db, contact_id, limit=MESSAGES_PER_PAGE, source='whatsapp')

    oldest_id = messages[0].id if messages else None
    more_above = has_messages_before(db, contact_id, oldest_id, source='whatsapp') if oldest_id else False

    today = date.today()
    yesterday = today - timedelta(days=1)

    return templates.TemplateResponse(
        request=request,
        name="history/index.html",
        context={
            "request": request,
            "contact": contact,
            "messages": messages,
            "has_more": more_above,
            "oldest_id": oldest_id,
            "today": today.strftime("%Y-%m-%d"),
            "yesterday": yesterday.strftime("%Y-%m-%d"),
        }
    )


@router.get("/{contact_id}/history/messages")
def get_more_messages(
    contact_id: int,
    before_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user or not get_contact_by_id(db, contact_id, current_user.id):
        return JSONResponse({"error": "unauthorized"}, status_code=401)

    messages = get_messages_before(db, contact_id, before_id, limit=MESSAGES_PER_PAGE, source='whatsapp')

    oldest_id = messages[0].id if messages else None
    more_above = has_messages_before(db, contact_id, oldest_id, source='whatsapp') if oldest_id else False

    def serialize(m):
        ts = m.created_at
        return {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "created_at": ts.isoformat() if ts else None,
        }

    return JSONResponse({
        "messages": [serialize(m) for m in messages],
        "has_more": more_above,
        "oldest_id": oldest_id,
    })
