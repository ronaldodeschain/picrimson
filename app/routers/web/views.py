from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime

router = APIRouter(tags=["Frontend"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "titulo": "Crimson Claw Studio",
        "versão": "1.0.0",
        "user": None,
        "is_admin": False,
        "year": datetime.utcnow().year,
    })

@router.get("/login.html", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "user": None,
        "is_admin": False,
        "is_auth": True,
        "year": datetime.utcnow().year,
    })