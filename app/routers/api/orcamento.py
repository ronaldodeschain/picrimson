from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.orcamento import Orcamento, OrcamentoCriarAtualizar
from app.repositories.orcamento import OrcamentoRepository
from app.dependencies import get_orcamento_repository

router = APIRouter(prefix="/orcamentos", tags=["Services"])

@router.get("/", response_model=List[Orcamento])
async def listar_orcamentos(repo: OrcamentoRepository = Depends(get_orcamento_repository)):
    return await repo.listar_orcamentos()

@router.get("/{orcamento_id}", response_model=Orcamento)
async def get_orcamento(orcamento_id: int, repo: OrcamentoRepository = Depends(get_orcamento_repository)):
    orcamento = await repo.get_orcamento(orcamento_id)
    if not orcamento:
        raise HTTPException(status_code=404, detail="Orcamento not found")
    return orcamento

@router.post("/", response_model=Orcamento)
async def criar_orcamento(orcamento: OrcamentoCriarAtualizar, repo: OrcamentoRepository = Depends(get_orcamento_repository)):
    return await repo.criar_orcamento(orcamento)

@router.put("/{orcamento_id}", response_model=Orcamento)
async def update_orcamento(orcamento_id: int, orcamento: OrcamentoCriarAtualizar, repo: OrcamentoRepository = Depends(get_orcamento_repository)):
    updated_orcamento = await repo.update_orcamento(orcamento_id, orcamento)
    if not updated_orcamento:
        raise HTTPException(status_code=404, detail="Orcamento not found")
    return updated_orcamento

@router.delete("/{orcamento_id}")
async def delete_orcamento(orcamento_id: int, repo: OrcamentoRepository = Depends(get_orcamento_repository)):
    deleted = await repo.delete_orcamento(orcamento_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Orcamento not found")
    return {"message": "Orcamento deleted successfully"}