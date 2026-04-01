from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models.pedido import PedidoCriarAtualizar
from app.repositories.pedido import PedidoRepository
import app.dependencies as dependencies

router = APIRouter(
    prefix="/pedido",
    tags=["Orders"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=list[PedidoCriarAtualizar])
async def listar_pedidos(
    pedido_repository: Annotated[PedidoRepository, Depends(
        dependencies.get_pedido_repository
    )]
):
    return await pedido_repository.listar_pedidos()

@router.get("/{pedido_id}", response_model=PedidoCriarAtualizar)
async def get_pedido(
    pedido_id: int,
    pedido_repository: Annotated[PedidoRepository, Depends(
        dependencies.get_pedido_repository
    )]
):
    pedido = await pedido_repository.get_pedido(pedido_id)

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

@router.post("/")
async def criar_pedido(
    pedido_repository: Annotated[PedidoRepository, Depends(
        dependencies.get_pedido_repository
    )],
    request: Request,
    valor_total: float,
    observacoes: str,
    id_pagamento: int,
    id_carrinho: int,
    id_cupom: int,
    id_servico: int
):
    pedido_criar = PedidoCriarAtualizar(
        valor_total=valor_total,
        observacoes=observacoes,
        id_pagamento=id_pagamento,
        id_carrinho=id_carrinho,
        id_cupom=id_cupom,
        id_servico=id_servico
    )
    pedido = await pedido_repository.criar_pedido(pedido_criar)
    return pedido

@router.put("/{pedido_id}", response_model=PedidoCriarAtualizar | None)
async def update_pedido(
    pedido_repository: Annotated[PedidoRepository, Depends(
        dependencies.get_pedido_repository
    )],
    pedido_id: int,
    pedido: PedidoCriarAtualizar
):
    pedido_atualizado = await pedido_repository.update_pedido(
        pedido_id, pedido
    )
    if not pedido_atualizado:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido_atualizado

@router.delete("/{pedido_id}", status_code=204)
async def delete_pedido(
    pedido_repository: Annotated[PedidoRepository, Depends(
        dependencies.get_pedido_repository
    )],
    pedido_id: int
):
    success = await pedido_repository.delete_pedido(pedido_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return RedirectResponse(url="/pedido", status_code=303)