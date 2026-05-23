from typing import Annotated
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.services.user_service import create_user
from app.dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])
templates =  Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def get_signup_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="users/signup.html",
        context={"request": request}
    )

@router.post("/", response_model=UserCreate)
def create_new_user(user: Annotated[UserCreate, Form()], db: Session = Depends(get_db)):
    return create_user(db, user)
