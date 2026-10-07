import os
import time
import smtplib
import shutil
from datetime import datetime, timezone
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Health"])


def _check_database() -> dict:
    start = time.monotonic()
    try:
        db_type = os.getenv("DATABASE_TYPE", "sqlite")
        if db_type == "postgres":
            from app.database.crimson_database_pg import Database
            db = Database()
            with db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
        else:
            from app.database.local import Database
            db = Database()
            with db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
        return {
            "status": "ok",
            "type": db_type,
            "latency_ms": round((time.monotonic() - start) * 1000, 2)
        }
    except Exception as e:
        return {
            "status": "error",
            "type": os.getenv("DATABASE_TYPE", "sqlite"),
            "error": str(e),
            "latency_ms": round((time.monotonic() - start) * 1000, 2)
        }


def _check_smtp() -> dict:
    start = time.monotonic()
    host = os.getenv("SMTP_SERVER") or os.getenv("EMAIL_SMTP_HOST", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT") or os.getenv("EMAIL_SMTP_PORT", "587"))
    user = os.getenv("SENDER_EMAIL") or os.getenv("EMAIL_SMTP_USER")
    password = os.getenv("SENDER_PASSWORD") or os.getenv("EMAIL_SMTP_PASSWORD")
    try:
        if not user or not password:
            return {"status": "not_configured", "host": host, "port": port}
        with smtplib.SMTP(host, port, timeout=5) as server:
            server.starttls()
            server.login(user, password)
        return {
            "status": "ok",
            "host": host,
            "port": port,
            "latency_ms": round((time.monotonic() - start) * 1000, 2)
        }
    except Exception as e:
        return {
            "status": "error",
            "host": host,
            "port": port,
            "error": str(e),
            "latency_ms": round((time.monotonic() - start) * 1000, 2)
        }


def _check_disk() -> dict:
    try:
        total, used, free = shutil.disk_usage(".")
        free_pct = round((free / total) * 100, 1)
        return {
            "status": "ok" if free_pct > 10 else "warning",
            "free_gb": round(free / (1024 ** 3), 2),
            "total_gb": round(total / (1024 ** 3), 2),
            "free_pct": free_pct
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def _check_uploads() -> dict:
    path = "app/static/uploads"
    try:
        exists = os.path.isdir(path)
        writable = os.access(path, os.W_OK) if exists else False
        return {
            "status": "ok" if (exists and writable) else "error",
            "path": path,
            "exists": exists,
            "writable": writable
        }
    except Exception as e:
        return {"status": "error", "path": path, "error": str(e)}


@router.get("/health")
async def health_simples():
    """Verificação rápida — usada por load balancers e Docker."""
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@router.get("/health/full")
async def health_completo():
    """Verificação completa de todos os componentes do sistema."""
    db = _check_database()
    smtp = _check_smtp()
    disk = _check_disk()
    uploads = _check_uploads()

    componentes = {"database": db, "smtp": smtp, "disk": disk, "uploads": uploads}

    # Status geral: degraded se algum não-crítico falhou, error se banco falhou
    if db["status"] == "error":
        status_geral = "error"
    elif any(v["status"] == "error" for v in [disk, uploads]):
        status_geral = "degraded"
    else:
        status_geral = "ok"

    http_status = 200 if status_geral == "ok" else (503 if status_geral == "error" else 207)

    return JSONResponse(
        status_code=http_status,
        content={
            "status": status_geral,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0",
            "environment": os.getenv("DATABASE_TYPE", "sqlite"),
            "components": componentes
        }
    )


@router.get("/health/db")
async def health_banco():
    """Verifica apenas a conexão com o banco de dados."""
    result = _check_database()
    return JSONResponse(
        status_code=200 if result["status"] == "ok" else 503,
        content=result
    )


@router.get("/health/smtp")
async def health_smtp():
    """Verifica apenas a conexão SMTP."""
    result = _check_smtp()
    return JSONResponse(
        status_code=200 if result["status"] in ("ok", "not_configured") else 503,
        content=result
    )
