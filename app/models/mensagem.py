from pydantic import BaseModel

class Mensagem(BaseModel):
    id_mensagem:int
    mensagem:str
    tipo_mensagem:str
    id_pedido:int
    id_email:int
    id_orcamento:int
    id_usuario:int
    id_nota_fiscal:int
    id_rastreio:int