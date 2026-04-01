from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models.categoria import CategoriaCriarAtualizar
from app.repositories.categoria import CategoriaRepository
import app.dependencies as dependencies

router = APIRouter(
    prefix="/categoria",
    tags=["Products"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=list[CategoriaCriarAtualizar])
async def listar_categorias(
    categoria_repository: Annotated[CategoriaRepository, Depends(
        dependencies.get_categoria_repository
    )]
):
    return await categoria_repository.listar_categorias()

@router.get("/{categoria_id}", response_model=CategoriaCriarAtualizar)
async def get_categoria(
    categoria_id: int,
    categoria_repository: Annotated[CategoriaRepository, Depends(
        dependencies.get_categoria_repository
    )]
):
    categoria = await categoria_repository.get_categoria(categoria_id)

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria

@router.post("/")
async def criar_categoria(
    categoria_repository: Annotated[CategoriaRepository, Depends(
        dependencies.get_categoria_repository
    )],
    request: Request,
    nome_categoria: str
):
    categoria_criar = CategoriaCriarAtualizar(
        nome_categoria=nome_categoria
    )
    categoria = await categoria_repository.criar_categoria(categoria_criar)
    return categoria

@router.put("/{categoria_id}", response_model=CategoriaCriarAtualizar | None)
async def update_categoria(
    categoria_repository: Annotated[CategoriaRepository, Depends(
        dependencies.get_categoria_repository
    )],
    categoria_id: int,
    categoria: CategoriaCriarAtualizar
):
    categoria_atualizada = await categoria_repository.update_categoria(
        categoria_id, categoria
    )
    if not categoria_atualizada:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria_atualizada

@router.delete("/{categoria_id}", status_code=204)
async def delete_categoria(
    categoria_repository: Annotated[CategoriaRepository, Depends(
        dependencies.get_categoria_repository
    )],
    categoria_id: int
):
    success = await categoria_repository.delete_categoria(categoria_id)
    if not success:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return RedirectResponse(url="/categoria", status_code=303)