from fastapi import FastAPI

from app.routers import usuario

app = FastAPI(
    title = "Crimson Claw Studio",
    description = "Backend para Projeto Integrador",
    version = "1.0.0"
)

app.include_router(usuario.router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}