from pydantic import BaseModel

class Rastreio(BaseModel):
    id_rastreio:int
    codigo_rastreio:int
    id_entrega:int
    id_mensagem:int