from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.item_pedido import ItemPedido, ItemPedidoCriarAtualizar
from app.repositories.item_pedido import ItemPedidoRepository
from app.dependencies import get_item_pedido_repository

router = APIRouter(prefix="/itens_pedido", tags=["Orders"])

@router.get("/", response_model=List[ItemPedido])
async def listar_itens_pedido(repo: ItemPedidoRepository = Depends(get_item_pedido_repository)):
    return await repo.listar_itens_pedido()

@router.get("/{item_id}", response_model=ItemPedido)
async def get_item_pedido(item_id: int, repo: ItemPedidoRepository = Depends(get_item_pedido_repository)):
    item = await repo.get_item_pedido(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="ItemPedido not found")
    return item

@router.post("/", response_model=ItemPedido)
async def criar_item_pedido(item: ItemPedidoCriarAtualizar, repo: ItemPedidoRepository = Depends(get_item_pedido_repository)):
    return await repo.criar_item_pedido(item)

@router.put("/{item_id}", response_model=ItemPedido)
async def update_item_pedido(item_id: int, item: ItemPedidoCriarAtualizar, repo: ItemPedidoRepository = Depends(get_item_pedido_repository)):
    updated_item = await repo.update_item_pedido(item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="ItemPedido not found")
    return updated_item

@router.delete("/{item_id}")
async def delete_item_pedido(item_id: int, repo: ItemPedidoRepository = Depends(get_item_pedido_repository)):
    deleted = await repo.delete_item_pedido(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="ItemPedido not found")
    return {"message": "ItemPedido deleted successfully"}