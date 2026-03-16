from pydantic import BaseModel

class Servico(BaseModel):
    id_servico:int
    tipo_servico:str
    valor_servico:float
    descricao:str
    id_pedido:int
    id_orcamento:int