from datetime import date
from typing import Optional
from pydantic import BaseModel

class Caixa(BaseModel):
    id_caixa: int
    tipo_movimentacao: str
    valor: float
    descricao: str
    data_movimentacao: Optional[date]
    id_nota_fiscal: int
    id_pagamento: int

class CaixaCriarAtualizar(BaseModel):
    tipo_movimentacao: str
    valor: float
    descricao: str
    data_movimentacao: Optional[date]
    id_nota_fiscal: int
    id_pagamento: int