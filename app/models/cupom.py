from pydantic import BaseModel

class Cupom(BaseModel):
    id_cupom:int
    chave_cupom:str
    valor_cupom:float
    tipo_cupom:str
    id_pedido:int