import os
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from app.autenticacao_middleware import DocsAuthMiddleware, SessionUserMiddleware

from app.routers.api import api_router
from app.routers.web import web_router

app = FastAPI(
    title = "Crimson Claw Studio",
    description = "Backend para Projeto Integrador",
    version = "1.0.0",
)

# Session support for logged-in users across page navigation
app.add_middleware(SessionUserMiddleware)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "super-secret-key"), session_cookie="crimson_session")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Adiciona o middleware de autenticação para as rotas de documetação
app.add_middleware(DocsAuthMiddleware)
# Inclui os agregadores de rotas
app.include_router(api_router, prefix="/api")
app.include_router(web_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}