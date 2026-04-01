from typing import Annotated, Optional
from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models.pagamento import PagamentoCriarAtualizar
from app.repositories.pagamento import PagamentoRepository
import app.dependencies as dependencies

router = APIRouter(
    prefix="/pagamento",
    tags=["Payments"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=list[PagamentoCriarAtualizar])
async def listar_pagamentos(
    pagamento_repository: Annotated[PagamentoRepository, Depends(
        dependencies.get_pagamento_repository
    )]
):
    return await pagamento_repository.listar_pagamentos()

@router.get("/{pagamento_id}", response_model=PagamentoCriarAtualizar)
async def get_pagamento(
    pagamento_id: int,
    pagamento_repository: Annotated[PagamentoRepository, Depends(
        dependencies.get_pagamento_repository
    )]
):
    pagamento = await pagamento_repository.get_pagamento(pagamento_id)

    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return pagamento

@router.post("/")
async def criar_pagamento(
    pagamento_repository: Annotated[PagamentoRepository, Depends(
        dependencies.get_pagamento_repository
    )],
    request: Request,
    expiracao: Optional[datetime] = None,
    valor_total: float = 0.0,
    data_pagamento: Optional[date] = None,
    pixTxid: str = "",
    id_pedido: int = 0,
    id_caixa: int = 0,
    id_nota_fiscal: int = 0,
    id_entrega: int = 0
):
    pagamento_criar = PagamentoCriarAtualizar(
        expiracao=expiracao,
        valor_total=valor_total,
        data_pagamento=data_pagamento,
        pixTxid=pixTxid,
        id_pedido=id_pedido,
        id_caixa=id_caixa,
        id_nota_fiscal=id_nota_fiscal,
        id_entrega=id_entrega
    )
    pagamento = await pagamento_repository.criar_pagamento(pagamento_criar)
    return pagamento

@router.put("/{pagamento_id}", response_model=PagamentoCriarAtualizar | None)
async def update_pagamento(
    pagamento_repository: Annotated[PagamentoRepository, Depends(
        dependencies.get_pagamento_repository
    )],
    pagamento_id: int,
    pagamento: PagamentoCriarAtualizar
):
    pagamento_atualizado = await pagamento_repository.update_pagamento(
        pagamento_id, pagamento
    )
    if not pagamento_atualizado:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return pagamento_atualizado

@router.delete("/{pagamento_id}", status_code=204)
async def delete_pagamento(
    pagamento_repository: Annotated[PagamentoRepository, Depends(
        dependencies.get_pagamento_repository
    )],
    pagamento_id: int
):
    success = await pagamento_repository.delete_pagamento(pagamento_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return RedirectResponse(url="/pagamento", status_code=303)