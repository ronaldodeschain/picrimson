import os
from typing import Annotated, Union
from fastapi import Depends

from app.database.local import Database
from app.database.postgres import PostgresDatabase
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
from app.repositories.pergunta import PerguntaRepository
from app.repositories.resposta import RespostaRepository

def get_database() -> Union[Database, PostgresDatabase]:
    if os.getenv("DATABASE_TYPE") == "postgres":
        return PostgresDatabase()
    return Database()

def get_usuario_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> UsuarioRepository:
    return UsuarioRepository(db)

def get_categoria_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> CategoriaRepository:
    return CategoriaRepository(db)

def get_produto_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> ProdutoRepository:
    return ProdutoRepository(db)

def get_pedido_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> PedidoRepository:
    return PedidoRepository(db)

def get_pagamento_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> PagamentoRepository:
    return PagamentoRepository(db)

def get_servico_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> ServicoRepository:
    return ServicoRepository(db)

def get_endereco_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> EnderecoRepository:
    return EnderecoRepository(db)

def get_telefone_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> TelefoneRepository:
    return TelefoneRepository(db)

def get_avaliacoes_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> AvaliacoesRepository:
    return AvaliacoesRepository(db)

def get_caixa_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> CaixaRepository:
    return CaixaRepository(db)

def get_carrinho_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> CarrinhoRepository:
    return CarrinhoRepository(db)

def get_cupom_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> CupomRepository:
    return CupomRepository(db)

def get_email_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> EmailRepository:
    return EmailRepository(db)

def get_pergunta_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> PerguntaRepository:
    return PerguntaRepository(db)

def get_resposta_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> RespostaRepository:
    return RespostaRepository(db)

def get_entrega_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> EntregaRepository:
    return EntregaRepository(db)

def get_favoritos_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> FavoritosRepository:
    return FavoritosRepository(db)

def get_imagem_produto_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> ImagemProdutoRepository:
    return ImagemProdutoRepository(db)

def get_item_pedido_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> ItemPedidoRepository:
    return ItemPedidoRepository(db)

def get_mensagem_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> MensagemRepository:
    return MensagemRepository(db)

def get_nota_fiscal_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> NotaFiscalRepository:
    return NotaFiscalRepository(db)

def get_orcamento_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> OrcamentoRepository:
    return OrcamentoRepository(db)

def get_rastreio_repository(
    db: Annotated[Union[Database, PostgresDatabase], Depends(get_database)]
) -> RastreioRepository:
    return RastreioRepository(db)