from datetime import datetime,date
from pydantic import BaseModel

class Pagamento(BaseModel):
    id_pagamento:int
    expiracao:datetime
    valor_total:float
    data_pagamento:date
    pixTxid:str
    id_pedido:int
    id_caixa:int
    id_nota_fiscal:int
    id_entrega:int