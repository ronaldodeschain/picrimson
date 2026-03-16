from pydantic import BaseModel

class Pedido(BaseModel):
    id_pedido:int
    valor_total:float
    observacoes:str
    id_pagamento:int
    id_carrinho:int
    id_cupom:int
    id_servico:int