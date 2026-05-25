from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.dependencies import get_current_user

router = APIRouter(tags=["dashboard"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
def get_dashboard(request: Request, current_user = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/users/login", status_code=303)
    
    return templates.TemplateResponse(
        request=request,
        name="dashboard/index.html",
        context={"request": request, "user": current_user}
    )