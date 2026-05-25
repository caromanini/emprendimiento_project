from typing import Annotated
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserLogin
from app.services.user_service import create_user, get_user_by_email, authenticate_user
from app.dependencies import get_db
from app.core.security import create_access_token

router = APIRouter(prefix="/users", tags=["users"])
templates =  Jinja2Templates(directory="app/templates")


@router.get("/signup", response_class=HTMLResponse)
def get_signup_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="users/signup.html",
        context={"request": request}
    )

@router.post("/signup", response_class=HTMLResponse)
def create_new_user(
    request: Request,
    user_credentials: Annotated[UserCreate, Form()],
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(db, user_credentials.email)
    if existing_user:
        return templates.TemplateResponse(
            request=request,
            name="users/signup.html",
            context={"request": request, "error": "Este correo ya está registrado."},
            status_code=400
        )
    
    create_user(db, user_credentials)

    return RedirectResponse(url="/users/login", status_code=303)

@router.get("/login", response_class=HTMLResponse)
def get_login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="users/login.html",
        context={"request": request}
    )

@router.post("/login", response_class=HTMLResponse)
def login_user(
    request: Request,
    user_credentials: Annotated[UserLogin, Form()],
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        return templates.TemplateResponse(
            request=request,
            name="users/login.html",
            context={"request": request, "error": "Correo o contraseña incorrectos."},
            status_code=400
        )
    
    access_token = create_access_token(data={"sub": user_credentials.email})
    response = RedirectResponse(url="/dashboard", status_code=303)

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=86400,
        secure=True,
        samesite="lax"
    )

    return response

@router.get("/logout", response_class=HTMLResponse)
def logout_user():
    response = RedirectResponse(url="/users/login", status_code=303)
    response.delete_cookie(key="access_token")
    
    return response