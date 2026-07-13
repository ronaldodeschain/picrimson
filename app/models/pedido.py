from pydantic import BaseModel
from typing import Optional

class Pedido(BaseModel):
    id_pedido:int
    valor_total:float
    observacoes:str
    id_pagamento:Optional[int] = None
    id_carrinho:Optional[int] = None
    id_cupom:Optional[int] = None
    id_servico:Optional[int] = None

class PedidoCriarAtualizar(BaseModel):
    valor_total:float
    observacoes:str
    id_pagamento:Optional[int] = None
    id_carrinho:Optional[int] = None
    id_cupom:Optional[int] = None
    id_servico:Optional[int] = None