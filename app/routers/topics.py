from typing import Annotated
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.schemas.topic import TopicCreate, TopicUpdate
from app.services.topic_service import (
    create_topic,
    delete_topic,
    get_topics_by_contact,
    get_topic_by_id,
    update_topic
)
from app.services.contact_service import get_contact_by_id
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/contacts", tags=["topics"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/{contact_id}/topics", response_class=HTMLResponse)
def get_topics_page(
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

    topics = get_topics_by_contact(db, contact_id)

    return templates.TemplateResponse(
        request=request,
        name="topics/index.html",
        context={"request": request, "contact": contact, "topics": topics}
    )

@router.post("/{contact_id}/topics", response_class=HTMLResponse)
def add_topic(
    request: Request, 
    contact_id: int, 
    topic: Annotated[TopicCreate, Form()], 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    if current_user and get_contact_by_id(db, contact_id, current_user.id):
        create_topic(db, topic, contact_id)
        
    return RedirectResponse(url=f"/contacts/{contact_id}/topics", status_code=303)

@router.get("/{contact_id}/topics/{topic_id}/edit", response_class=HTMLResponse)
def get_edit_topic_page(
    request: Request,
    topic_id: int,
    contact_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user or not get_contact_by_id(db, contact_id, current_user.id):
        return RedirectResponse(url="/dashboard", status_code=303)
        
    topic = get_topic_by_id(db, topic_id)
    if not topic or topic.contact_id != contact_id:
        return RedirectResponse(url=f"/contacts/{contact_id}/topics", status_code=303)
        
    return templates.TemplateResponse(
        request=request,
        name="topics/edit.html",
        context={"request": request, "topic": topic, "contact_id": contact_id}
    )

@router.post("/{contact_id}/topics/{topic_id}/edit", response_class=HTMLResponse)
def edit_topic(
    request: Request,
    topic_id: int,
    contact_id: int,
    topic_data: Annotated[TopicUpdate, Form()],
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user and get_contact_by_id(db, contact_id, current_user.id):
        update_topic(db, topic_id, topic_data)
        
    return RedirectResponse(url=f"/contacts/{contact_id}/topics", status_code=303)

@router.post("/{contact_id}/topics/{topic_id}/delete", response_class=HTMLResponse)
def remove_topic(
    request: Request, 
    topic_id: int, 
    contact_id: int, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    if current_user and get_contact_by_id(db, contact_id, current_user.id):
        delete_topic(db, topic_id)
        
    return RedirectResponse(url=f"/contacts/{contact_id}/topics", status_code=303)
