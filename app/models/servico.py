from pydantic import BaseModel
from typing import Optional

class Servico(BaseModel):
    id_servico:int
    tipo_servico:str
    valor_servico:float
    descricao:str
    id_pedido:Optional[int] = None
    id_orcamento:Optional[int] = None

class ServicoCriarAtualizar(BaseModel):
    tipo_servico:str
    valor_servico:float
    descricao:str
    id_pedido:Optional[int] = None
    id_orcamento:Optional[int] = None