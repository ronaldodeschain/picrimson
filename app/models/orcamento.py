from pydantic import BaseModel

class Orcamento(BaseModel):
    id_orcamento:int
    mensagem:str
    arquivo:str
    imagem:str
    id_mensagem:int
    id_servico:int