from datetime import date
from pydantic import BaseModel
from typing import Optional

class NotaFiscal(BaseModel):
    id_nota_fiscal:int
    forma_pagamento:str
    data_emissao:date
    serie:str
    numero:int
    status:str
    id_caixa:Optional[int] = None
    id_pagamento:Optional[int] = None
    id_mensagem:Optional[int] = None

class NotaFiscalCriarAtualizar(BaseModel):
    forma_pagamento:str
    data_emissao:date
    serie:str
    numero:int
    status:str
    id_caixa:Optional[int] = None
    id_pagamento:Optional[int] = None
    id_mensagem:Optional[int] = None