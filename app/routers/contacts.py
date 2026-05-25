from typing import Annotated
from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.schemas.contact import ContactCreate, ContactUpdate
from app.services.contact_service import (
    create_contact, get_contact_by_id, update_contact, delete_contact
)
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/contacts", tags=["contacts"])
templates = Jinja2Templates(directory="app/templates")

@router.post("/add", response_class=HTMLResponse)
def add_new_contact(
    request: Request,
    contact: Annotated[ContactCreate, Form()],
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse(url="/users/login", status_code=303)
    
    create_contact(db, contact, current_user.id)

    return RedirectResponse(url="/dashboard", status_code=303)

@router.get("/edit/{contact_id}", response_class=HTMLResponse)
def get_edit_contact_page(
    request: Request,
    contact_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse(url="/users/login", status_code=303)
    
    contact = get_contact_by_id(db, contact_id, current_user.id)
    if not contact:
        return RedirectResponse(url="/dashboard", status_code=303)
        
    return templates.TemplateResponse(
        request=request,
        name="contacts/edit.html",
        context={"request": request, "contact": contact}
    )

@router.post("/edit/{contact_id}", response_class=HTMLResponse)
def edit_contact(
    request: Request,
    contact_id: int,
    contact_data: Annotated[ContactUpdate, Form()],
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse(url="/users/login", status_code=303)

    update_contact(db, contact_id, current_user.id, contact_data)
    
    return RedirectResponse(url="/dashboard", status_code=303)

@router.post("/delete/{contact_id}", response_class=HTMLResponse)
def delete_existing_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse(url="/users/login", status_code=303)
        
    delete_contact(db, contact_id, current_user.id)
    
    return RedirectResponse(url="/dashboard", status_code=303)