from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.services.contact_service import get_user_contacts

router = APIRouter(tags=["dashboard"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
def get_dashboard(
    request: Request,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user:
        return RedirectResponse(url="/users/login", status_code=303)
    
    user_contacts = get_user_contacts(db, current_user.id)

    return templates.TemplateResponse(
        request=request,
        name="dashboard/index.html",
        context={"request": request, "user": current_user, "contacts": user_contacts}
    )