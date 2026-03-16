from datetime import date
from pydantic import BaseModel

class Entrega(BaseModel):
    id_entrega:int
    mensagem:str
    tipo_mensagem:str
    data_entrega_prevista:date
    data_envio:date
    tipo_entrega:str
    endereco_entrega:str
    observacoes:str
    data_pedido:date
    status_entrega:str
    id_pedido:int
    id_rastreio:int
    