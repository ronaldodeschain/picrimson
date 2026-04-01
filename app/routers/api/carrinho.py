from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models.carrinho import CarrinhoCriarAtualizar
from app.repositories.carrinho import CarrinhoRepository
import app.dependencies as dependencies

router = APIRouter(
    prefix="/carrinho",
    tags=["Orders"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=list[CarrinhoCriarAtualizar])
async def listar_carrinhos(
    carrinho_repository: Annotated[CarrinhoRepository, Depends(
        dependencies.get_carrinho_repository
    )]
):
    return await carrinho_repository.listar_carrinhos()

@router.get("/{carrinho_id}", response_model=CarrinhoCriarAtualizar)
async def get_carrinho(
    carrinho_id: int,
    carrinho_repository: Annotated[CarrinhoRepository, Depends(
        dependencies.get_carrinho_repository
    )]
):
    carrinho = await carrinho_repository.get_carrinho(carrinho_id)

    if not carrinho:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")
    return carrinho

@router.post("/")
async def criar_carrinho(
    carrinho_repository: Annotated[CarrinhoRepository, Depends(
        dependencies.get_carrinho_repository
    )],
    request: Request,
    id_servico: int,
    id_pedido: int,
    id_item_pedido: int,
    id_usuario: int
):
    carrinho_criar = CarrinhoCriarAtualizar(
        id_servico=id_servico,
        id_pedido=id_pedido,
        id_item_pedido=id_item_pedido,
        id_usuario=id_usuario
    )
    carrinho = await carrinho_repository.criar_carrinho(carrinho_criar)
    return carrinho

@router.put("/{carrinho_id}", response_model=CarrinhoCriarAtualizar | None)
async def update_carrinho(
    carrinho_repository: Annotated[CarrinhoRepository, Depends(
        dependencies.get_carrinho_repository
    )],
    carrinho_id: int,
    carrinho: CarrinhoCriarAtualizar
):
    carrinho_atualizado = await carrinho_repository.update_carrinho(
        carrinho_id, carrinho
    )
    if not carrinho_atualizado:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")
    return carrinho_atualizado

@router.delete("/{carrinho_id}", status_code=204)
async def delete_carrinho(
    carrinho_repository: Annotated[CarrinhoRepository, Depends(
        dependencies.get_carrinho_repository
    )],
    carrinho_id: int
):
    success = await carrinho_repository.delete_carrinho(carrinho_id)
    if not success:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")
    return RedirectResponse(url="/carrinho", status_code=303)