import asyncio
from unittest.mock import AsyncMock

import pytest

from app.models.imagem_produto import ImagemProdutoCriarAtualizar
from app.models.produto import Produto, ProdutoCriarAtualizar
from app.services.produto_service import ProdutoService


class FakeProdutoRepository:
    def __init__(self, produto: Produto | None = None):
        self.criar_produto = AsyncMock(return_value=produto)


class FakeImagemProdutoRepository:
    def __init__(self):
        self.criar_imagem_produto = AsyncMock(return_value=None)


def test_cadastrar_produto_valido_com_imagem_url():
    """CT-008: deve cadastrar produto com todos os campos válidos e imagem_url aceita."""
    produto = Produto(
        id_produto=1,
        nome_produto="Miniatura de Dragão",
        descricao="Miniatura pintada à mão",
        material="Resina",
        altura=12.0,
        comprimento=7.0,
        largura=5.0,
        quantidade=10,
        peso=0.5,
        valor=199.90,
        id_categoria=2,
        imagens=[],
    )
    produto_repo = FakeProdutoRepository(produto)
    imagem_repo = FakeImagemProdutoRepository()
    service = ProdutoService(produto_repo, imagem_repo)

    dados = ProdutoCriarAtualizar(
        nome_produto="Miniatura de Dragão",
        descricao="Miniatura pintada à mão",
        material="Resina",
        altura=12.0,
        comprimento=7.0,
        largura=5.0,
        quantidade=10,
        peso=0.5,
        valor=199.90,
        id_categoria=2,
    )
    image_url = "https://example.com/produto.png"

    produto_criado, erro = asyncio.run(service.cadastrar_produto(dados, image_url=image_url))

    assert erro is None
    assert produto_criado is produto
    produto_repo.criar_produto.assert_awaited_once_with(dados)
    imagem_repo.criar_imagem_produto.assert_awaited_once()

    imagem_criada = imagem_repo.criar_imagem_produto.call_args.args[0]
    assert isinstance(imagem_criada, ImagemProdutoCriarAtualizar)
    assert imagem_criada.nome_imagem == dados.nome_produto
    assert imagem_criada.arquivo_imagem == image_url
    assert imagem_criada.id_produto == produto.id_produto


@pytest.mark.parametrize("invalid_value", [0, -10])
def test_cadastrar_produto_preco_invalido(invalid_value):
    """CT-010: deve bloquear cadastro quando o preço for zero ou negativo."""
    produto_repo = FakeProdutoRepository(produto=None)
    imagem_repo = FakeImagemProdutoRepository()
    service = ProdutoService(produto_repo, imagem_repo)

    dados = ProdutoCriarAtualizar(
        nome_produto="Miniatura de Dragão",
        descricao="Miniatura pintada à mão",
        material="Resina",
        altura=12.0,
        comprimento=7.0,
        largura=5.0,
        quantidade=5,
        peso=0.5,
        valor=invalid_value,
        id_categoria=2,
    )

    produto_criado, erro = asyncio.run(service.cadastrar_produto(dados, image_url="https://example.com/produto.png"))

    assert produto_criado is None
    assert erro == "O preço do produto deve ser maior que zero."
    produto_repo.criar_produto.assert_not_awaited()
    imagem_repo.criar_imagem_produto.assert_not_awaited()


def test_cadastrar_produto_nome_vazio():
    """CT-009: deve bloquear cadastro quando o nome do produto estiver vazio."""
    produto_repo = FakeProdutoRepository(produto=None)
    imagem_repo = FakeImagemProdutoRepository()
    service = ProdutoService(produto_repo, imagem_repo)

    dados = ProdutoCriarAtualizar(
        nome_produto="  ",
        descricao="Miniatura pintada à mão",
        material="Resina",
        altura=12.0,
        comprimento=7.0,
        largura=5.0,
        quantidade=5,
        peso=0.5,
        valor=199.90,
        id_categoria=2,
    )

    produto_criado, erro = asyncio.run(service.cadastrar_produto(dados, image_url="https://example.com/produto.png"))

    assert produto_criado is None
    assert erro == "O nome do produto é obrigatório."
    produto_repo.criar_produto.assert_not_awaited()
    imagem_repo.criar_imagem_produto.assert_not_awaited()


def test_cadastrar_produto_estoque_invalido():
    """CT-011: deve bloquear cadastro quando o estoque for negativo."""
    produto_repo = FakeProdutoRepository(produto=None)
    imagem_repo = FakeImagemProdutoRepository()
    service = ProdutoService(produto_repo, imagem_repo)

    dados = ProdutoCriarAtualizar(
        nome_produto="Miniatura de Dragão",
        descricao="Miniatura pintada à mão",
        material="Resina",
        altura=12.0,
        comprimento=7.0,
        largura=5.0,
        quantidade=-1,
        peso=0.5,
        valor=199.90,
        id_categoria=2,
    )

    produto_criado, erro = asyncio.run(service.cadastrar_produto(dados, image_url="https://example.com/produto.png"))

    assert produto_criado is None
    assert erro == "A quantidade do produto não pode ser negativa."
    produto_repo.criar_produto.assert_not_awaited()
    imagem_repo.criar_imagem_produto.assert_not_awaited()
