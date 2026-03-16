from pydantic import BaseModel

class ItemPedido(BaseModel):
    id_item_pedido:int
    id_usuario:int
    id_produto:int
    id_carrinho:int