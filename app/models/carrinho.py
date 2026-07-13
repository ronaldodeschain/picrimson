from pydantic import BaseModel
from typing import Optional

class Carrinho(BaseModel):
    id_carrinho:int
    id_servico:Optional[int] = None
    id_pedido:Optional[int] = None
    id_item_pedido:Optional[int] = None
    id_usuario:int

class CarrinhoCriarAtualizar(BaseModel):
    id_servico:Optional[int] = None
    id_pedido:Optional[int] = None
    id_item_pedido:Optional[int] = None
    id_usuario:int