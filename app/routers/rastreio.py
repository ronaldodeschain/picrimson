from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.rastreio import Rastreio, RastreioCriarAtualizar
from app.repositories.rastreio import RastreioRepository
from app.dependencies import get_rastreio_repository

router = APIRouter(prefix="/rastreios", tags=["Shipping"])

@router.get("/", response_model=List[Rastreio])
async def listar_rastreios(repo: RastreioRepository = Depends(get_rastreio_repository)):
    return await repo.listar_rastreios()

@router.get("/{rastreio_id}", response_model=Rastreio)
async def get_rastreio(rastreio_id: int, repo: RastreioRepository = Depends(get_rastreio_repository)):
    rastreio = await repo.get_rastreio(rastreio_id)
    if not rastreio:
        raise HTTPException(status_code=404, detail="Rastreio not found")
    return rastreio

@router.post("/", response_model=Rastreio)
async def criar_rastreio(rastreio: RastreioCriarAtualizar, repo: RastreioRepository = Depends(get_rastreio_repository)):
    return await repo.criar_rastreio(rastreio)

@router.put("/{rastreio_id}", response_model=Rastreio)
async def update_rastreio(rastreio_id: int, rastreio: RastreioCriarAtualizar, repo: RastreioRepository = Depends(get_rastreio_repository)):
    updated_rastreio = await repo.update_rastreio(rastreio_id, rastreio)
    if not updated_rastreio:
        raise HTTPException(status_code=404, detail="Rastreio not found")
    return updated_rastreio

@router.delete("/{rastreio_id}")
async def delete_rastreio(rastreio_id: int, repo: RastreioRepository = Depends(get_rastreio_repository)):
    deleted = await repo.delete_rastreio(rastreio_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Rastreio not found")
    return {"message": "Rastreio deleted successfully"}