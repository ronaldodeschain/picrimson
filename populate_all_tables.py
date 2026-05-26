import asyncio
from datetime import date
from app.dependencies import get_database
from app.repositories.usuario import UsuarioRepository
from app.repositories.categoria import CategoriaRepository
from app.repositories.produto import ProdutoRepository
from app.repositories.imagem_produto import ImagemProdutoRepository
from app.repositories.item_pedido import ItemPedidoRepository
from app.repositories.nota_fiscal import NotaFiscalRepository
from app.repositories.endereco import EnderecoRepository
from app.repositories.orcamento import OrcamentoRepository
from app.repositories.avaliacoes import AvaliacoesRepository
from app.repositories.pagamento import PagamentoRepository
from app.repositories.pedido import PedidoRepository
from app.repositories.cupom import CupomRepository
from app.repositories.rastreio import RastreioRepository
from app.repositories.caixa import CaixaRepository
from app.repositories.email import EmailRepository
from app.repositories.carrinho import CarrinhoRepository
from app.repositories.servico import ServicoRepository
from app.repositories.mensagem import MensagemRepository
from app.repositories.telefone import TelefoneRepository
from app.repositories.favoritos import FavoritosRepository
from app.repositories.entrega import EntregaRepository
from app.repositories.pergunta import PerguntaRepository
from app.repositories.resposta import RespostaRepository

from app.models.usuario import UsuarioCriarAtualizar
from app.models.categoria import CategoriaCriarAtualizar
from app.models.produto import ProdutoCriarAtualizar
from app.models.imagem_produto import ImagemProdutoCriarAtualizar
from app.models.item_pedido import ItemPedidoCriarAtualizar
from app.models.nota_fiscal import NotaFiscalCriarAtualizar
from app.models.endereco import EnderecoCriarAtualizar
from app.models.orcamento import OrcamentoCriarAtualizar
from app.models.avaliacoes import AvaliacoesCriarAtualizar
from app.models.pagamento import PagamentoCriarAtualizar
from app.models.pedido import PedidoCriarAtualizar
from app.models.cupom import CupomCriarAtualizar
from app.models.rastreio import RastreioCriarAtualizar
from app.models.caixa import CaixaCriarAtualizar
from app.models.email import EmailCriarAtualizar
from app.models.carrinho import CarrinhoCriarAtualizar
from app.models.servico import ServicoCriarAtualizar
from app.models.mensagem import MensagemCriarAtualizar
from app.models.telefone import TelefoneCriarAtualizar
from app.models.favoritos import FavoritosCriarAtualizar
from app.models.entrega import EntregaCriarAtualizar
from app.models.pergunta import PerguntaCriarAtualizar
from app.models.resposta import RespostaCriarAtualizar

async def populate_all_tables():
    db = get_database()
    usuario_repo = UsuarioRepository(db)
    categoria_repo = CategoriaRepository(db)
    produto_repo = ProdutoRepository(db)
    imagem_produto_repo = ImagemProdutoRepository(db)
    item_pedido_repo = ItemPedidoRepository(db)
    nota_fiscal_repo = NotaFiscalRepository(db)
    endereco_repo = EnderecoRepository(db)
    orcamento_repo = OrcamentoRepository(db)
    avaliacoes_repo = AvaliacoesRepository(db)
    pagamento_repo = PagamentoRepository(db)
    pedido_repo = PedidoRepository(db)
    cupom_repo = CupomRepository(db)
    rastreio_repo = RastreioRepository(db)
    caixa_repo = CaixaRepository(db)
    email_repo = EmailRepository(db)
    carrinho_repo = CarrinhoRepository(db)
    servico_repo = ServicoRepository(db)
    mensagem_repo = MensagemRepository(db)
    telefone_repo = TelefoneRepository(db)
    favoritos_repo = FavoritosRepository(db)
    entrega_repo = EntregaRepository(db)
    pergunta_repo = PerguntaRepository(db)
    resposta_repo = RespostaRepository(db)

    # Populate usuarios
    for i in range(1, 6):
        usuario = UsuarioCriarAtualizar(
            nome_usuario=f"Usuario {i}",
            login=f"user{i}",
            senha=f"senha{i}",
            cpf=f"123456789{i:02d}",
            role="user"
        )
        await usuario_repo.criar_usuario(usuario)

    # Create Admin user
    admin_usuario = UsuarioCriarAtualizar(
        nome_usuario="Admin",
        login="admin",
        senha="admin123",
        cpf="00000000000",
        role="admin"
    )
    admin_criado = await usuario_repo.criar_usuario(admin_usuario)
    if admin_criado and admin_criado.id_usuario:
        await email_repo.criar_email(
            EmailCriarAtualizar(
                email="admin@crimson.com",
                id_usuario=admin_criado.id_usuario
            )
        )

    # Populate categorias
    for i in range(1, 6):
        categoria = CategoriaCriarAtualizar(
            nome_categoria=f"Categoria {i}"
        )
        await categoria_repo.criar_categoria(categoria)

    # Populate produtos
    for i in range(1, 6):
        produto = ProdutoCriarAtualizar(
            nome_produto=f"Produto {i}",
            descricao=f"Descrição do produto {i}",
            material=f"Material {i}",
            altura=10.0 + i,
            comprimento=20.0 + i,
            largura=5.0 + i,
            quantidade=100 + i,
            peso=1.5 + i,
            valor=50.0 + i * 10,
            id_categoria=i
        )
        await produto_repo.criar_produto(produto)

    # Populate imagem_produtos
    for i in range(1, 6):
        imagem_produto = ImagemProdutoCriarAtualizar(
            nome_imagem=f"Imagem {i}",
            arquivo_imagem=f"https://picsum.photos/id/{i+10}/600/400",
            id_produto=i
        )
        await imagem_produto_repo.criar_imagem_produto(imagem_produto)

    # Populate item_pedidos
    for i in range(1, 6):
        item_pedido = ItemPedidoCriarAtualizar(
            id_usuario=i,
            id_produto=i,
            id_carrinho=1  # Assuming carrinho will be inserted later, using dummy value
        )
        await item_pedido_repo.criar_item_pedido(item_pedido)

    # Populate notas_fiscais
    for i in range(1, 6):
        nota_fiscal = NotaFiscalCriarAtualizar(
            forma_pagamento=f"Forma {i}",
            data_emissao=date(2023,1,i),
            serie=f"Serie {i}",
            numero=1000 + i,
            status="Emitida",
            id_caixa=1,
            id_pagamento=1,
            id_mensagem=1
        )
        await nota_fiscal_repo.criar_nota_fiscal(nota_fiscal)

    # Populate enderecos
    for i in range(1, 6):
        endereco = EnderecoCriarAtualizar(
            rua=f"Rua {i}",
            numero=100 + i,
            complemento=f"Apt {i}",
            cep=f"12345-0{i:02d}",
            cidade=f"Cidade {i}",
            estado=f"Estado {i}",
            observacoes=f"Obs {i}",
            id_usuario=i
        )
        await endereco_repo.criar_endereco(endereco)

    # Populate orcamentos
    for i in range(1, 6):
        orcamento = OrcamentoCriarAtualizar(
            mensagem=f"Mensagem {i}",
            arquivo=f"arquivo{i}.pdf",
            imagem=f"imagem{i}.jpg",
            id_mensagem=1,
            id_servico=1
        )
        await orcamento_repo.criar_orcamento(orcamento)

    # Populate avaliacoes
    for i in range(1, 6):
        avaliacao = AvaliacoesCriarAtualizar(
            comentario=f"Comentário {i}",
            avaliacao=4.5 + (i % 2) * 0.5,
            id_produto=i,
            id_usuario=i
        )
        await avaliacoes_repo.criar_avaliacao(avaliacao)

    # Populate pagamentos
    for i in range(1, 6):
        pagamento = PagamentoCriarAtualizar(
            expiracao=None,
            valor_total=200.0 + i * 30,
            data_pagamento=None,
            pixTxid=f"txid{i}",
            id_pedido=1,
            id_caixa=1,
            id_nota_fiscal=1,
            id_entrega=1
        )
        await pagamento_repo.criar_pagamento(pagamento)

    # Populate pedidos
    for i in range(1, 6):
        pedido = PedidoCriarAtualizar(
            valor_total=150.0 + i * 25,
            observacoes=f"Obs {i}",
            id_pagamento=1,
            id_carrinho=1,
            id_cupom=1,
            id_servico=1
        )
        await pedido_repo.criar_pedido(pedido)

    # Populate cupons
    for i in range(1, 6):
        cupom = CupomCriarAtualizar(
            chave_cupom=f"CUPOM{i}",
            valor_cupom=10.0 + i,
            tipo_cupom="Desconto",
            id_pedido=1
        )
        await cupom_repo.criar_cupom(cupom)

    # Populate rastreio
    for i in range(1, 6):
        rastreio = RastreioCriarAtualizar(
            codigo_rastreio=123456789 + i,
            id_entrega=1,
            id_mensagem=1
        )
        await rastreio_repo.criar_rastreio(rastreio)

    # Populate caixa
    for i in range(1, 6):
        caixa = CaixaCriarAtualizar(
            tipo_movimentacao="Entrada" if i % 2 == 0 else "Saida",
            valor=50.0 + i * 5,
            descricao=f"Descrição {i}",
            data_movimentacao=None,
            id_nota_fiscal=1,
            id_pagamento=1
        )
        await caixa_repo.criar_caixa(caixa)

    # Populate email
    for i in range(1, 6):
        email = EmailCriarAtualizar(
            email=f"user{i}@example.com",
            id_usuario=i
        )
        await email_repo.criar_email(email)

    # Populate carrinho
    for i in range(1, 6):
        carrinho = CarrinhoCriarAtualizar(
            id_servico=1,
            id_pedido=1,
            id_item_pedido=1,
            id_usuario=i
        )
        await carrinho_repo.criar_carrinho(carrinho)

    # Populate servico
    for i in range(1, 6):
        servico = ServicoCriarAtualizar(
            tipo_servico=f"Tipo {i}",
            valor_servico=100.0 + i * 15,
            descricao=f"Descrição {i}",
            id_pedido=1,
            id_orcamento=1
        )
        await servico_repo.criar_servico(servico)

    # Populate mensagem
    for i in range(1, 6):
        mensagem = MensagemCriarAtualizar(
            mensagem=f"Mensagem {i}",
            tipo_mensagem="Info",
            id_pedido=1,
            id_email=1,
            id_orcamento=1,
            id_usuario=i,
            id_nota_fiscal=1,
            id_rastreio=1
        )
        await mensagem_repo.criar_mensagem(mensagem)

    # Populate telefone
    for i in range(1, 6):
        telefone = TelefoneCriarAtualizar(
            telefone_principal=1198765432 + i,
            telefone_secundario=1187654321 + i,
            id_usuario=i
        )
        await telefone_repo.criar_telefone(telefone)

    # Populate favoritos
    for i in range(1, 6):
        favorito = FavoritosCriarAtualizar(
            id_produto=i,
            id_usuario=i
        )
        await favoritos_repo.criar_favorito(favorito)

    # Populate entrega
    for i in range(1, 6):
        entrega = EntregaCriarAtualizar(
            mensagem=f"Mensagem entrega {i}",
            tipo_mensagem="Entrega",
            data_entrega_prevista=date(2023,4,i),
            data_envio=date(2023,3,i),
            tipo_entrega="Correios",
            endereco_entrega=f"Endereço {i}",
            observacoes=f"Obs {i}",
            data_pedido=date(2023,3,i),
            status_entrega="Enviado",
            id_pedido=1,
            id_rastreio=1
        )
        await entrega_repo.criar_entrega(entrega)

    # Populate pergunta
    for i in range(1, 6):
        pergunta = PerguntaCriarAtualizar(
            pergunta=f"Pergunta {i}",
            data_criacao=f"2023-05-{i:02d}",
            id_usuario=i,
            id_produto=i,
            id_resposta=i
        )
        await pergunta_repo.criar_pergunta(pergunta)

    # Populate resposta
    for i in range(1, 6):
        resposta = RespostaCriarAtualizar(
            texto_resposta=f"Resposta {i}",
            data_resposta=f"2023-05-{i:02d}",
            id_usuario=i,
            id_produto=i,
            id_pergunta=i
        )
        await resposta_repo.criar_resposta(resposta)

    print("Todas as tabelas foram populadas com 5 registros cada.")

if __name__ == "__main__":
    asyncio.run(populate_all_tables())