from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

from app.routers.api import api_router
from app.routers.web import web_router

app = FastAPI(
    title = "Crimson Claw Studio",
    description = "Backend para Projeto Integrador",
    version = "1.0.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Inclui os agregadores de rotas
app.include_router(api_router, prefix="/api")
app.include_router(web_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}