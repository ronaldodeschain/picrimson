from pydantic import BaseModel
from typing import Optional

class Mensagem(BaseModel):
    id_mensagem:int
    mensagem:str
    tipo_mensagem:str
    id_pedido:Optional[int] = None
    id_email:Optional[int] = None
    id_orcamento:Optional[int] = None
    id_usuario:Optional[int] = None
    id_nota_fiscal:Optional[int] = None
    id_rastreio:Optional[int] = None

class MensagemCriarAtualizar(BaseModel):
    mensagem:str
    tipo_mensagem:str
    id_pedido:Optional[int] = None
    id_email:Optional[int] = None
    id_orcamento:Optional[int] = None
    id_usuario:Optional[int] = None
    id_nota_fiscal:Optional[int] = None
    id_rastreio:Optional[int] = None