from datetime import date
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.services.contact_service import get_contact_by_id
from app.services.report_service import get_all_reports, get_report_by_date

router = APIRouter(prefix="/contacts", tags=["reports"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/{contact_id}/reports", response_class=HTMLResponse)
def list_reports(
    request: Request, 
    contact_id: int, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    if not current_user or not get_contact_by_id(db, contact_id, current_user.id):
        return RedirectResponse(url="/dashboard", status_code=303)

    contact = get_contact_by_id(db, contact_id, current_user.id)
    reports = get_all_reports(db, contact_id)

    return templates.TemplateResponse(
        request=request,
        name="reports/index.html",
        context={"request": request, "contact": contact, "reports": reports}
    )

@router.get("/{contact_id}/reports/{report_date}", response_class=HTMLResponse)
def get_report_detail(
    request: Request, 
    contact_id: int, 
    report_date: date,
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    if not current_user or not get_contact_by_id(db, contact_id, current_user.id):
        return RedirectResponse(url="/dashboard", status_code=303)

    contact = get_contact_by_id(db, contact_id, current_user.id)
    report = get_report_by_date(db, contact_id, report_date)

    return templates.TemplateResponse(
        request=request,
        name="reports/detail.html",
        context={
            "request": request,
            "contact": contact,
            "report": report,
            "target_date": report_date
        }
    )
