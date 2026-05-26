import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from app.autenticacao_middleware import DocsAuthMiddleware, SessionUserMiddleware

from app.routers.api import api_router
from app.routers.web import web_router
from app.routers.web.admin import router as admin_web_router

app = FastAPI(
    title = "Crimson Claw Studio",
    description = "Backend para Projeto Integrador",
    version = "1.0.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Adiciona o middleware de autenticação para as rotas de documetação
app.add_middleware(DocsAuthMiddleware)

# Session support for logged-in users across page navigation
app.add_middleware(SessionUserMiddleware)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "super-secret-key"), session_cookie="crimson_session")

# Inclui os agregadores de rotas
app.include_router(api_router, prefix="/api")
app.include_router(web_router)
app.include_router(admin_web_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.exception_handler(401)
async def unauthorized_redirect_handler(request: Request, exc: HTTPException):
    """Redireciona para o login em caso de erro 401 (não autenticado)."""
    return RedirectResponse(url="/login.html", status_code=303)