from pydantic import BaseModel
from typing import Optional

class Rastreio(BaseModel):
    id_rastreio:int
    codigo_rastreio:int
    id_entrega:int
    id_mensagem:Optional[int] = None

class RastreioCriarAtualizar(BaseModel):
    codigo_rastreio:int
    id_entrega:int
    id_mensagem:Optional[int] = None