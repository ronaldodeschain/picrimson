from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.favoritos import Favoritos, FavoritosCriarAtualizar
from app.repositories.favoritos import FavoritosRepository
from app.dependencies import get_favoritos_repository

router = APIRouter(prefix="/favoritos", tags=["Products"])

@router.get("/", response_model=List[Favoritos])
async def listar_favoritos(repo: FavoritosRepository = Depends(get_favoritos_repository)):
    return await repo.listar_favoritos()

@router.get("/{favorito_id}", response_model=Favoritos)
async def get_favorito(favorito_id: int, repo: FavoritosRepository = Depends(get_favoritos_repository)):
    favorito = await repo.get_favorito(favorito_id)
    if not favorito:
        raise HTTPException(status_code=404, detail="Favorito not found")
    return favorito

@router.post("/", response_model=Favoritos)
async def criar_favorito(favorito: FavoritosCriarAtualizar, repo: FavoritosRepository = Depends(get_favoritos_repository)):
    return await repo.criar_favorito(favorito)

@router.put("/{favorito_id}", response_model=Favoritos)
async def update_favorito(favorito_id: int, favorito: FavoritosCriarAtualizar, repo: FavoritosRepository = Depends(get_favoritos_repository)):
    updated_favorito = await repo.update_favorito(favorito_id, favorito)
    if not updated_favorito:
        raise HTTPException(status_code=404, detail="Favorito not found")
    return updated_favorito

@router.delete("/{favorito_id}")
async def delete_favorito(favorito_id: int, repo: FavoritosRepository = Depends(get_favoritos_repository)):
    deleted = await repo.delete_favorito(favorito_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Favorito not found")
    return {"message": "Favorito deleted successfully"}