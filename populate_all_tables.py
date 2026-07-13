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

    # 1. Usuarios (sem dependências)
    usuario_ids = []
    for i in range(1, 6):
        u = await usuario_repo.criar_usuario(UsuarioCriarAtualizar(
            nome_usuario=f"Usuario {i}",
            login=f"user{i}",
            senha=f"senha{i}",
            cpf=f"1234567{i:04d}",
            role="user"
        ))
        usuario_ids.append(u.id_usuario)

    admin = await usuario_repo.criar_usuario(UsuarioCriarAtualizar(
        nome_usuario="Admin",
        login="admin",
        senha="admin123",
        cpf="00000000000",
        autenticado="autenticado",
        role="admin"
    ))

    # 2. Email (depende de usuario)
    email_ids = []
    for i, uid in enumerate(usuario_ids, 1):
        e = await email_repo.criar_email(EmailCriarAtualizar(
            email=f"user{i}@example.com",
            id_usuario=uid
        ))
        email_ids.append(e.id_email)

    await email_repo.criar_email(EmailCriarAtualizar(
        email="admin@crimson.com",
        id_usuario=admin.id_usuario
    ))

    # 3. Endereco (depende de usuario)
    for i, uid in enumerate(usuario_ids, 1):
        await endereco_repo.criar_endereco(EnderecoCriarAtualizar(
            rua=f"Rua {i}",
            numero=100 + i,
            complemento=f"Apt {i}",
            cep=f"12345-{i:03d}",
            cidade=f"Cidade {i}",
            estado="SP",
            observacoes=f"Obs {i}",
            id_usuario=uid
        ))

    # 4. Telefone (depende de usuario)
    for i, uid in enumerate(usuario_ids, 1):
        await telefone_repo.criar_telefone(TelefoneCriarAtualizar(
            telefone_principal=f"1198765{i:04d}",
            telefone_secundario=f"1187654{i:04d}",
            id_usuario=uid
        ))

    # 5. Categorias (sem dependências)
    categoria_ids = []
    for i in range(1, 6):
        c = await categoria_repo.criar_categoria(CategoriaCriarAtualizar(
            nome_categoria=f"Categoria {i}"
        ))
        categoria_ids.append(c.id_categoria)

    # 6. Produtos (depende de categoria)
    produto_ids = []
    for i, cid in enumerate(categoria_ids, 1):
        p = await produto_repo.criar_produto(ProdutoCriarAtualizar(
            nome_produto=f"Produto {i}",
            descricao=f"Descrição do produto {i}",
            material=f"Material {i}",
            altura=10.0 + i,
            comprimento=20.0 + i,
            largura=5.0 + i,
            quantidade=100 + i,
            peso=1.5 + i,
            valor=50.0 + i * 10,
            id_categoria=cid
        ))
        produto_ids.append(p.id_produto)

    # 7. Imagem produtos (depende de produto)
    for i, pid in enumerate(produto_ids, 1):
        await imagem_produto_repo.criar_imagem_produto(ImagemProdutoCriarAtualizar(
            nome_imagem=f"Imagem {i}",
            arquivo_imagem=f"https://picsum.photos/id/{i+10}/600/400",
            id_produto=pid
        ))

    # 8. Avaliacoes (depende de produto e usuario)
    for i, (pid, uid) in enumerate(zip(produto_ids, usuario_ids), 1):
        await avaliacoes_repo.criar_avaliacao(AvaliacoesCriarAtualizar(
            comentario=f"Comentário {i}",
            avaliacao=4.5 + (i % 2) * 0.5,
            id_produto=pid,
            id_usuario=uid
        ))

    # 9. Favoritos (depende de produto e usuario)
    for pid, uid in zip(produto_ids, usuario_ids):
        await favoritos_repo.criar_favorito(FavoritosCriarAtualizar(
            id_produto=pid,
            id_usuario=uid
        ))

    # 10. Orcamentos (sem FK obrigatória inicialmente — id_mensagem e id_servico são opcionais)
    orcamento_ids = []
    for i in range(1, 6):
        o = await orcamento_repo.criar_orcamento(OrcamentoCriarAtualizar(
            mensagem=f"Mensagem {i}",
            arquivo=f"arquivo{i}.pdf",
            imagem=f"imagem{i}.jpg",
            nome=f"Cliente {i}",
            contato=f"contato{i}@email.com",
            tipo_projeto=f"Tipo {i}",
            descricao=f"Descrição {i}",
            tamanho_desejado=f"Tamanho {i}"
        ))
        orcamento_ids.append(o.id_orcamento)

    # 11. Servico (depende de orcamento; id_pedido pode ser None inicialmente)
    servico_ids = []
    for i, oid in enumerate(orcamento_ids, 1):
        s = await servico_repo.criar_servico(ServicoCriarAtualizar(
            tipo_servico=f"Tipo {i}",
            valor_servico=100.0 + i * 15,
            descricao=f"Descrição {i}",
            id_pedido=None,
            id_orcamento=oid
        ))
        servico_ids.append(s.id_servico)

    # 12. Cupons (id_pedido pode ser None inicialmente)
    cupom_ids = []
    for i in range(1, 6):
        c = await cupom_repo.criar_cupom(CupomCriarAtualizar(
            chave_cupom=f"CUPOM{i}",
            valor_cupom=10.0 + i,
            tipo_cupom="Desconto",
            id_pedido=None
        ))
        cupom_ids.append(c.id_cupom)

    # 13. Entrega (id_pedido e id_rastreio podem ser None inicialmente)
    entrega_ids = []
    for i in range(1, 6):
        e = await entrega_repo.criar_entrega(EntregaCriarAtualizar(
            mensagem=f"Mensagem entrega {i}",
            tipo_mensagem="Entrega",
            data_entrega_prevista=date(2023, 4, i),
            data_envio=date(2023, 3, i),
            tipo_entrega="Correios",
            endereco_entrega=f"Endereço {i}",
            observacoes=f"Obs {i}",
            data_pedido=date(2023, 3, i),
            status_entrega="Enviado",
            id_pedido=None,
            id_rastreio=None
        ))
        entrega_ids.append(e.id_entrega)

    # 14. Rastreio (depende de entrega)
    rastreio_ids = []
    for i, eid in enumerate(entrega_ids, 1):
        r = await rastreio_repo.criar_rastreio(RastreioCriarAtualizar(
            codigo_rastreio=123456789 + i,
            id_entrega=eid,
            id_mensagem=None
        ))
        rastreio_ids.append(r.id_rastreio)

    # 15. Pagamentos (depende de entrega; id_pedido, id_caixa, id_nota_fiscal podem ser None)
    pagamento_ids = []
    for i, (eid, rid) in enumerate(zip(entrega_ids, rastreio_ids), 1):
        p = await pagamento_repo.criar_pagamento(PagamentoCriarAtualizar(
            expiracao=None,
            valor_total=200.0 + i * 30,
            data_pagamento=None,
            pixTxid=f"txid{i}",
            id_pedido=None,
            id_caixa=None,
            id_nota_fiscal=None,
            id_entrega=eid
        ))
        pagamento_ids.append(p.id_pagamento)

    # 16. Pedidos (depende de pagamento, servico, cupom; id_carrinho pode ser None)
    pedido_ids = []
    for i, (pgid, sid, cuid) in enumerate(zip(pagamento_ids, servico_ids, cupom_ids), 1):
        p = await pedido_repo.criar_pedido(PedidoCriarAtualizar(
            valor_total=150.0 + i * 25,
            observacoes=f"Obs {i}",
            id_pagamento=pgid,
            id_carrinho=None,
            id_cupom=cuid,
            id_servico=sid
        ))
        pedido_ids.append(p.id_pedido)

    # 17. Carrinho (depende de usuario, pedido, servico; id_item_pedido pode ser None)
    carrinho_ids = []
    for i, (uid, pid, sid) in enumerate(zip(usuario_ids, pedido_ids, servico_ids), 1):
        c = await carrinho_repo.criar_carrinho(CarrinhoCriarAtualizar(
            id_servico=sid,
            id_pedido=pid,
            id_item_pedido=None,
            id_usuario=uid
        ))
        carrinho_ids.append(c.id_carrinho)

    # 18. Item pedidos (depende de usuario, produto, carrinho)
    item_ids = []
    for uid, pid, cid in zip(usuario_ids, produto_ids, carrinho_ids):
        it = await item_pedido_repo.criar_item_pedido(ItemPedidoCriarAtualizar(
            id_usuario=uid,
            id_produto=pid,
            id_carrinho=cid
        ))
        item_ids.append(it.id_item_pedido)

    # 19. Notas fiscais (depende de caixa, pagamento, mensagem — caixa e mensagem ainda None)
    nota_fiscal_ids = []
    for i, pgid in enumerate(pagamento_ids, 1):
        nf = await nota_fiscal_repo.criar_nota_fiscal(NotaFiscalCriarAtualizar(
            forma_pagamento=f"Forma {i}",
            data_emissao=date(2023, 1, i),
            serie=f"Serie {i}",
            numero=1000 + i,
            status="Emitida",
            id_caixa=None,
            id_pagamento=pgid,
            id_mensagem=None
        ))
        nota_fiscal_ids.append(nf.id_nota_fiscal)

    # 20. Caixa (depende de nota_fiscal e pagamento)
    caixa_ids = []
    for i, (nfid, pgid) in enumerate(zip(nota_fiscal_ids, pagamento_ids), 1):
        cx = await caixa_repo.criar_caixa(CaixaCriarAtualizar(
            tipo_movimentacao="Entrada" if i % 2 == 0 else "Saida",
            valor=50.0 + i * 5,
            descricao=f"Descrição {i}",
            data_movimentacao=None,
            id_nota_fiscal=nfid,
            id_pagamento=pgid
        ))
        caixa_ids.append(cx.id_caixa)

    # 21. Mensagem (depende de pedido, email, orcamento, usuario, nota_fiscal, rastreio)
    mensagem_ids = []
    for i, (pid, eid, oid, uid, nfid, rid) in enumerate(
        zip(pedido_ids, email_ids, orcamento_ids, usuario_ids, nota_fiscal_ids, rastreio_ids), 1
    ):
        m = await mensagem_repo.criar_mensagem(MensagemCriarAtualizar(
            mensagem=f"Mensagem {i}",
            tipo_mensagem="Info",
            id_pedido=pid,
            id_email=eid,
            id_orcamento=oid,
            id_usuario=uid,
            id_nota_fiscal=nfid,
            id_rastreio=rid
        ))
        mensagem_ids.append(m.id_mensagem)

    # 22. Resposta (depende de usuario e produto; id_pergunta pode ser None)
    resposta_ids = []
    for i, (uid, pid) in enumerate(zip(usuario_ids, produto_ids), 1):
        r = await resposta_repo.criar_resposta(RespostaCriarAtualizar(
            texto_resposta=f"Resposta {i}",
            data_resposta=f"2023-05-{i:02d}",
            id_usuario=uid,
            id_produto=pid,
            id_pergunta=None
        ))
        resposta_ids.append(r.id_resposta)

    # 23. Pergunta (depende de usuario, produto, resposta)
    for i, (uid, pid, rid) in enumerate(zip(usuario_ids, produto_ids, resposta_ids), 1):
        await pergunta_repo.criar_pergunta(PerguntaCriarAtualizar(
            pergunta=f"Pergunta {i}",
            data_criacao=f"2023-05-{i:02d}",
            id_usuario=uid,
            id_produto=pid,
            id_resposta=rid
        ))

    print("Todas as tabelas foram populadas com 5 registros cada.")

if __name__ == "__main__":
    asyncio.run(populate_all_tables())
