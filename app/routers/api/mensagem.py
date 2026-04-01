from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.mensagem import Mensagem, MensagemCriarAtualizar
from app.repositories.mensagem import MensagemRepository
from app.dependencies import get_mensagem_repository

router = APIRouter(prefix="/mensagens", tags=["Communication"])

@router.get("/", response_model=List[Mensagem])
async def listar_mensagens(repo: MensagemRepository = Depends(get_mensagem_repository)):
    return await repo.listar_mensagens()

@router.get("/{mensagem_id}", response_model=Mensagem)
async def get_mensagem(mensagem_id: int, repo: MensagemRepository = Depends(get_mensagem_repository)):
    mensagem = await repo.get_mensagem(mensagem_id)
    if not mensagem:
        raise HTTPException(status_code=404, detail="Mensagem not found")
    return mensagem

@router.post("/", response_model=Mensagem)
async def criar_mensagem(mensagem: MensagemCriarAtualizar, repo: MensagemRepository = Depends(get_mensagem_repository)):
    return await repo.criar_mensagem(mensagem)

@router.put("/{mensagem_id}", response_model=Mensagem)
async def update_mensagem(mensagem_id: int, mensagem: MensagemCriarAtualizar, repo: MensagemRepository = Depends(get_mensagem_repository)):
    updated_mensagem = await repo.update_mensagem(mensagem_id, mensagem)
    if not updated_mensagem:
        raise HTTPException(status_code=404, detail="Mensagem not found")
    return updated_mensagem

@router.delete("/{mensagem_id}")
async def delete_mensagem(mensagem_id: int, repo: MensagemRepository = Depends(get_mensagem_repository)):
    deleted = await repo.delete_mensagem(mensagem_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Mensagem not found")
    return {"message": "Mensagem deleted successfully"}