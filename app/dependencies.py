from typing import Annotated
from fastapi import Depends

from app.database.local import Database
from app.repositories.usuario import UsuarioRepository
from app.repositories.categoria import CategoriaRepository
from app.repositories.produto import ProdutoRepository
from app.repositories.pedido import PedidoRepository
from app.repositories.pagamento import PagamentoRepository
from app.repositories.servico import ServicoRepository
from app.repositories.endereco import EnderecoRepository
from app.repositories.telefone import TelefoneRepository
from app.repositories.avaliacoes import AvaliacoesRepository
from app.repositories.caixa import CaixaRepository
from app.repositories.carrinho import CarrinhoRepository
from app.repositories.cupom import CupomRepository
from app.repositories.email import EmailRepository
from app.repositories.entrega import EntregaRepository
from app.repositories.favoritos import FavoritosRepository
from app.repositories.imagem_produto import ImagemProdutoRepository
from app.repositories.item_pedido import ItemPedidoRepository
from app.repositories.mensagem import MensagemRepository
from app.repositories.nota_fiscal import NotaFiscalRepository
from app.repositories.orcamento import OrcamentoRepository
from app.repositories.rastreio import RastreioRepository


db = Database()

def get_database() -> Database:
    return db

def get_usuario_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> UsuarioRepository:
    return UsuarioRepository(Local_db)

def get_categoria_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> CategoriaRepository:
    return CategoriaRepository(Local_db)

def get_produto_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> ProdutoRepository:
    return ProdutoRepository(Local_db)

def get_pedido_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> PedidoRepository:
    return PedidoRepository(Local_db)

def get_pagamento_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> PagamentoRepository:
    return PagamentoRepository(Local_db)

def get_servico_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> ServicoRepository:
    return ServicoRepository(Local_db)

def get_endereco_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> EnderecoRepository:
    return EnderecoRepository(Local_db)

def get_telefone_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> TelefoneRepository:
    return TelefoneRepository(Local_db)

def get_avaliacoes_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> AvaliacoesRepository:
    return AvaliacoesRepository(Local_db)

def get_caixa_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> CaixaRepository:
    return CaixaRepository(Local_db)

def get_carrinho_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> CarrinhoRepository:
    return CarrinhoRepository(Local_db)

def get_cupom_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> CupomRepository:
    return CupomRepository(Local_db)

def get_email_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> EmailRepository:
    return EmailRepository(Local_db)

def get_entrega_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> EntregaRepository:
    return EntregaRepository(Local_db)

def get_favoritos_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> FavoritosRepository:
    return FavoritosRepository(Local_db)

def get_imagem_produto_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> ImagemProdutoRepository:
    return ImagemProdutoRepository(Local_db)

def get_item_pedido_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> ItemPedidoRepository:
    return ItemPedidoRepository(Local_db)

def get_mensagem_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> MensagemRepository:
    return MensagemRepository(Local_db)

def get_nota_fiscal_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> NotaFiscalRepository:
    return NotaFiscalRepository(Local_db)

def get_orcamento_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> OrcamentoRepository:
    return OrcamentoRepository(Local_db)

def get_rastreio_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> RastreioRepository:
    return RastreioRepository(Local_db)