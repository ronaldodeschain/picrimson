from fastapi import APIRouter
from . import (
    usuario, categoria, produto, pedido, pagamento, servico, 
    endereco, telefone, avaliacao, caixa, carrinho, cupom, 
    email, entrega, favoritos, imagem_produto, item_pedido, 
    mensagem, nota_fiscal, orcamento, rastreio, pergunta, resposta
)

api_router = APIRouter()

api_router.include_router(usuario.router)
api_router.include_router(categoria.router)
api_router.include_router(produto.router)
api_router.include_router(mensagem.router)
api_router.include_router(entrega.router)
api_router.include_router(rastreio.router)
api_router.include_router(orcamento.router)
api_router.include_router(pedido.router)
api_router.include_router(pagamento.router)
api_router.include_router(servico.router)
api_router.include_router(endereco.router)
api_router.include_router(telefone.router)
api_router.include_router(avaliacao.router)
api_router.include_router(caixa.router)
api_router.include_router(carrinho.router)
api_router.include_router(cupom.router)
api_router.include_router(email.router)
api_router.include_router(favoritos.router)
api_router.include_router(imagem_produto.router)
api_router.include_router(item_pedido.router)
api_router.include_router(nota_fiscal.router)
api_router.include_router(pergunta.router)
api_router.include_router(resposta.router)