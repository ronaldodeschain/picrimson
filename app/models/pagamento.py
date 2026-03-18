from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel

class Pagamento(BaseModel):
    id_pagamento: int
    expiracao: Optional[datetime]
    valor_total: float
    data_pagamento: Optional[date]
    pixTxid: str
    id_pedido: int
    id_caixa: int
    id_nota_fiscal: int
    id_entrega: int

class PagamentoCriarAtualizar(BaseModel):
    expiracao: Optional[datetime]
    valor_total: float
    data_pagamento: Optional[date]
    pixTxid: str
    id_pedido: int
    id_caixa: int
    id_nota_fiscal: int
    id_entrega: int