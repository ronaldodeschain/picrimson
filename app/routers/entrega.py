from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.entrega import Entrega, EntregaCriarAtualizar
from app.repositories.entrega import EntregaRepository
from app.dependencies import get_entrega_repository

router = APIRouter(prefix="/entregas", tags=["Shipping"])

@router.get("/", response_model=List[Entrega])
async def listar_entregas(repo: EntregaRepository = Depends(get_entrega_repository)):
    return await repo.listar_entregas()

@router.get("/{entrega_id}", response_model=Entrega)
async def get_entrega(entrega_id: int, repo: EntregaRepository = Depends(get_entrega_repository)):
    entrega = await repo.get_entrega(entrega_id)
    if not entrega:
        raise HTTPException(status_code=404, detail="Entrega not found")
    return entrega

@router.post("/", response_model=Entrega)
async def criar_entrega(entrega: EntregaCriarAtualizar, repo: EntregaRepository = Depends(get_entrega_repository)):
    return await repo.criar_entrega(entrega)

@router.put("/{entrega_id}", response_model=Entrega)
async def update_entrega(entrega_id: int, entrega: EntregaCriarAtualizar, repo: EntregaRepository = Depends(get_entrega_repository)):
    updated_entrega = await repo.update_entrega(entrega_id, entrega)
    if not updated_entrega:
        raise HTTPException(status_code=404, detail="Entrega not found")
    return updated_entrega

@router.delete("/{entrega_id}")
async def delete_entrega(entrega_id: int, repo: EntregaRepository = Depends(get_entrega_repository)):
    deleted = await repo.delete_entrega(entrega_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Entrega not found")
    return {"message": "Entrega deleted successfully"}