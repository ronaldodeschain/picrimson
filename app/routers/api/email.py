from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.email import Email, EmailCriarAtualizar
from app.repositories.email import EmailRepository
from app.dependencies import get_email_repository

router = APIRouter(prefix="/emails", tags=["User Management"])

@router.get("/", response_model=List[Email])
async def listar_emails(repo: EmailRepository = Depends(get_email_repository)):
    return await repo.listar_emails()

@router.get("/{id_email}", response_model=Email)
async def get_email(id_email: int, repo: EmailRepository = Depends(get_email_repository)):
    email = await repo.get_email(id_email)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email

@router.post("/", response_model=Email)
async def criar_email(email: EmailCriarAtualizar, repo: EmailRepository = Depends(get_email_repository)):
    return await repo.criar_email(email)

@router.put("/{id_email}", response_model=Email)
async def update_email(id_email: int, email: EmailCriarAtualizar, repo: EmailRepository = Depends(get_email_repository)):
    updated_email = await repo.update_email(id_email, email)
    if not updated_email:
        raise HTTPException(status_code=404, detail="Email not found")
    return updated_email

@router.delete("/{id_email}")
async def delete_email(id_email: int, repo: EmailRepository = Depends(get_email_repository)):
    deleted = await repo.delete_email(id_email)
    if not deleted:
        raise HTTPException(status_code=404, detail="Email not found")
    return {"message": "Email deleted successfully"}