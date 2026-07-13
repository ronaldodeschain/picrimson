from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel

class Pagamento(BaseModel):
    id_pagamento: int
    expiracao: Optional[datetime] = None
    valor_total: float
    data_pagamento: Optional[date] = None
    pixTxid: str
    id_pedido: Optional[int] = None
    id_caixa: Optional[int] = None
    id_nota_fiscal: Optional[int] = None
    id_entrega: Optional[int] = None

class PagamentoCriarAtualizar(BaseModel):
    expiracao: Optional[datetime] = None
    valor_total: float
    data_pagamento: Optional[date] = None
    pixTxid: str
    id_pedido: Optional[int] = None
    id_caixa: Optional[int] = None
    id_nota_fiscal: Optional[int] = None
    id_entrega: Optional[int] = None