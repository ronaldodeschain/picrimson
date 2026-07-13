from pydantic import BaseModel
from typing import Optional

class Cupom(BaseModel):
    id_cupom:int
    chave_cupom:str
    valor_cupom:float
    tipo_cupom:str
    id_pedido:Optional[int] = None

class CupomCriarAtualizar(BaseModel):
    chave_cupom:str
    valor_cupom:float
    tipo_cupom:str
    id_pedido:Optional[int] = None