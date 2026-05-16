from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.autenticacao_middleware import DocsAuthMiddleware

from app.routers.api import api_router
from app.routers.web import web_router

app = FastAPI(
    title = "Crimson Claw Studio",
    description = "Backend para Projeto Integrador",
    version = "1.0.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Adiciona o middleware de autenticação para as rotas de documetação
app.add_middleware(DocsAuthMiddleware)
# Inclui os agregadores de rotas
app.include_router(api_router, prefix="/api")
app.include_router(web_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}