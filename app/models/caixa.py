from datetime import date
from pydantic import BaseModel

class Caixa(BaseModel):
    id_caixa:int
    tipo_movimentacao:str
    valor:float
    descricao:str
    data_movimentacao:date
    id_nota_fiscal:int
    id_pagamento:int