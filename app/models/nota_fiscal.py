from datetime import date
from pydantic import BaseModel

class NotaFiscal(BaseModel):
    id_nota_fiscal:int
    forma_pagamento:str
    data_emissao:date
    serie:str
    numero:int
    status:str
    id_caixa:int
    id_pagamento:int
    id_mensagem:int