from typing import Annotated
from fastapi import APIRouter, Request, Depends, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from pathlib import Path
from uuid import uuid4
from app.repositories.produto import ProdutoRepository
from app.repositories.imagem_produto import ImagemProdutoRepository
from app.repositories.avaliacoes import AvaliacoesRepository
from app.repositories.usuario import UsuarioRepository
from app.repositories.email import EmailRepository
import app.dependencies as dependencies

router = APIRouter(tags=["Frontend"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    produto_repo: Annotated[ProdutoRepository, Depends(dependencies.get_produto_repository)]
):
    produtos = await produto_repo.listar_produtos()
    return templates.TemplateResponse("home.html", {
        "request": request,
        "titulo": "Crimson Claw Studio",
        "produtos": produtos,
        "user": None,
        "is_admin": False,
        "year": datetime.utcnow().year,
    })

@router.get("/login.html", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "user": None,
        "is_admin": False,
        "email": "",
        "password": "",
        "error": None,
        "is_auth": True,
        "year": datetime.utcnow().year,
    })


@router.post("/login.html", response_class=HTMLResponse)
async def login_submit(
    request: Request,
    email_repo: Annotated[EmailRepository, Depends(dependencies.get_email_repository)],
    usuario_repo: Annotated[UsuarioRepository, Depends(dependencies.get_usuario_repository)],
    email: str = Form(...),
    password: str = Form(...),
):
    # Lookup the email record first (login by real email address)
    email_obj = await email_repo.get_email_por_valor(email)
    if not email_obj:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "user": None,
            "is_admin": False,
            "email": email,
            "password": "",
            "error": "Email ou senha inválidos.",
            "is_auth": True,
            "year": datetime.utcnow().year,
        })

    usuario = await usuario_repo.get_cliente(email_obj.id_usuario)
    if not usuario or usuario.senha != password:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "user": None,
            "is_admin": False,
            "email": email,
            "password": "",
            "error": "Email ou senha inválidos.",
            "is_auth": True,
            "year": datetime.utcnow().year,
        })

    pedidos = []
    orcamentos = []
    return templates.TemplateResponse("minha_conta.html", {
        "request": request,
        "user": usuario,
        "is_admin": usuario.role == "admin",
        "pedidos": pedidos,
        "orcamentos": orcamentos,
        "year": datetime.utcnow().year,
    })


@router.get("/produtos", response_class=HTMLResponse)
async def produtos(
    request: Request,
    produto_repo: Annotated[ProdutoRepository, Depends(dependencies.get_produto_repository)],
    categoria_repo: Annotated[dependencies.CategoriaRepository, Depends(dependencies.get_categoria_repository)],
    categoria: str | None = None,
    preco_min: str | None = None,
    preco_max: str | None = None,
    material: str | None = None,
    pintado: str | None = None,
):
    categorias = await categoria_repo.listar_categorias()

    def parse_float(value: str | None) -> float | None:
        if value is None or value == "":
            return None
        try:
            return float(value)
        except ValueError:
            return None

    preco_min_val = parse_float(preco_min)
    preco_max_val = parse_float(preco_max)
    cat_id = None
    if categoria:
        try:
            cat_id = int(categoria)
        except ValueError:
            cat_id = None

    produtos = await produto_repo.listar_produtos(
        categoria=cat_id,
        preco_min=preco_min_val,
        preco_max=preco_max_val,
        material=material
    )

    return templates.TemplateResponse("products.html", {
        "request": request,
        "titulo": "Produtos",
        "produtos": produtos,
        "categorias": categorias,
        "user": None,
        "is_admin": False,
        "year": datetime.utcnow().year,
    })


@router.get("/produto/{produto_id}", response_class=HTMLResponse)
async def produto_detail(
    request: Request,
    produto_id: int,
    produto_repo: Annotated[ProdutoRepository, Depends(dependencies.get_produto_repository)],
    imagem_repo: Annotated[ImagemProdutoRepository, Depends(dependencies.get_imagem_produto_repository)]
):
    produto = await produto_repo.get_produto(produto_id)
    imagens = await imagem_repo.listar_imagens_produto()
    imagens_prod = [img for img in imagens if img.id_produto == produto_id]
    if not produto:
        return templates.TemplateResponse("home.html", {"request": request, "titulo": "Produto não encontrado", "produtos": [], "user": None, "is_admin": False, "year": datetime.utcnow().year})
    return templates.TemplateResponse("product.html", {
        "request": request,
        "titulo": produto.nome_produto,
        "produto": produto,
        "imagens": imagens_prod,
        "user": None,
        "is_admin": False,
        "year": datetime.utcnow().year,
    })


@router.get("/orcamento", response_class=HTMLResponse)
async def orcamento(request: Request):
    tipos_projeto = [
        "Impressão 3D personalizável",
        "Modelagem 3D",
        "Pintura artística/manual",
        "Projeto para RPG ou diorama"
    ]
    return templates.TemplateResponse("orcamento.html", {
        "request": request,
        "titulo": "Orçamento",
        "tipos_projeto": tipos_projeto,
        "success": False,
        "user": None,
        "is_admin": False,
        "year": datetime.utcnow().year,
    })


@router.post("/orcamento", response_class=HTMLResponse)
async def orcamento_submit(
    request: Request,
    orcamento_repo: Annotated[dependencies.OrcamentoRepository, Depends(dependencies.get_orcamento_repository)],
    nome: str = Form(...),
    contato: str = Form(...),
    tipo_projeto: str = Form(...),
    descricao: str = Form(...),
    tamanho_desejado: str = Form(...),
    arquivo: UploadFile | None = File(None),
):
    upload_path = None
    if arquivo and arquivo.filename:
        uploads_dir = Path("app/static/uploads")
        uploads_dir.mkdir(parents=True, exist_ok=True)
        safe_name = f"{uuid4().hex}_{arquivo.filename}"
        target_path = uploads_dir / safe_name
        with target_path.open("wb") as buffer:
            buffer.write(await arquivo.read())
        upload_path = f"/static/uploads/{safe_name}"

    from app.models.orcamento import OrcamentoCriarAtualizar
    novo_orcamento = OrcamentoCriarAtualizar(
        nome=nome,
        contato=contato,
        tipo_projeto=tipo_projeto,
        descricao=descricao,
        tamanho_desejado=tamanho_desejado,
        arquivo=upload_path,
        mensagem=None,
        imagem=None,
        id_mensagem=None,
        id_servico=None
    )
    await orcamento_repo.criar_orcamento(novo_orcamento)
    tipos_projeto = [
        "Impressão 3D personalizável",
        "Modelagem 3D",
        "Pintura artística/manual",
        "Projeto para RPG ou diorama"
    ]
    return templates.TemplateResponse("orcamento.html", {
        "request": request,
        "titulo": "Orçamento",
        "tipos_projeto": tipos_projeto,
        "success": True,
        "nome": nome,
        "user": None,
        "is_admin": False,
        "year": datetime.utcnow().year,
    })


@router.get("/sobre", response_class=HTMLResponse)
async def sobre(
    request: Request,
    avaliacoes_repo: Annotated[AvaliacoesRepository, Depends(dependencies.get_avaliacoes_repository)],
):
    testemunhos = await avaliacoes_repo.listar_avaliacoes_com_usuario()
    valores = [
        "Criamos peças únicas para colecionadores apaixonados por mundos fantásticos.",
        "Unimos arte e tecnologia para transformar conceitos em miniaturas, acessórios e decoração premium.",
        "Cada projeto é criado com foco em detalhe, acabamento e personalidade.",
    ]
    etapas = [
        {
            "titulo": "Como começou",
            "texto": "O Crimson Claw nasceu da paixão por mesas de RPG, personagens lendários e o desejo de levar arte impressa para colecionadores." 
        },
        {
            "titulo": "Por que impressão 3D",
            "texto": "A impressão 3D permite criar formas complexas e personalizar cada peça para narrativas únicas e coleções com alma." 
        },
        {
            "titulo": "Nosso diferencial",
            "texto": "Combinamos conhecimento artístico e tecnologia para entregar miniaturas, dioramas e acessórios com acabamento premium." 
        }
    ]
    equipamentos = [
        {
            "nome": "Impressora resinada de alta resolução",
            "detalhe": "Detalhes finos, camadas invisíveis e superfícies prontas para pintura." 
        },
        {
            "nome": "Estação de pintura artesanal",
            "detalhe": "Técnicas manuais, bases texturizadas e efeitos de luz realistas." 
        },
        {
            "nome": "Fluxo digital completo",
            "detalhe": "Modelagem, revisão técnica e preparação de arquivos prontos para produção." 
        }
    ]
    return templates.TemplateResponse("sobre.html", {
        "request": request,
        "titulo": "Sobre",
        "valores": valores,
        "etapas": etapas,
        "equipamentos": equipamentos,
        "testemunhos": testemunhos,
        "user": None,
        "is_admin": False,
        "year": datetime.utcnow().year,
    })


@router.get("/cadastro", response_class=HTMLResponse)
async def cadastro(request: Request):
    return templates.TemplateResponse("cadastro.html", {
        "request": request,
        "user": None,
        "is_admin": False,
        "error": None,
        "success": False,
        "nome": "",
        "email": "",
        "cpf": "",
        "year": datetime.utcnow().year,
    })


@router.post("/cadastro", response_class=HTMLResponse)
async def cadastro_submit(
    request: Request,
    usuario_repo: Annotated[UsuarioRepository, Depends(dependencies.get_usuario_repository)],
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    cpf: str = Form(...),
):
    from app.models.usuario import UsuarioCriarAtualizar
    novo_usuario = UsuarioCriarAtualizar(
        nome_usuario=nome,
        login=email,
        senha=senha,
        cpf=cpf,
        role="user"
    )
    usuario = await usuario_repo.criar_usuario(novo_usuario)
    # also create email row linking to the new usuario so login by email works
    from app.models.email import EmailCriarAtualizar
    email_repo: Annotated[EmailRepository, Depends(dependencies.get_email_repository)]
    # create email entry (if repository available)
    try:
        email_model = EmailCriarAtualizar(email=email, id_usuario=usuario.id_usuario)  # type: ignore
        # use low-level call to repository to avoid changing signature: instantiate repo here
        email_repo_instance = EmailRepository(dependencies.get_database())
        await email_repo_instance.criar_email(email_model)
    except Exception:
        pass
    return templates.TemplateResponse("cadastro.html", {
        "request": request,
        "user": None,
        "is_admin": False,
        "success": True,
        "error": None,
        "nome": nome,
        "email": email,
        "cpf": cpf,
        "year": datetime.utcnow().year,
    })


@router.get("/minha-conta", response_class=HTMLResponse)
async def minha_conta(request: Request):
    return templates.TemplateResponse("minha_conta.html", {
        "request": request,
        "user": None,
        "is_admin": False,
        "pedidos": [],
        "orcamentos": [],
        "year": datetime.utcnow().year,
    })


@router.get("/servicos", response_class=HTMLResponse)
async def servicos(request: Request):
    servicos = [
        {
            "titulo": "Impressão 3D sob medida",
            "descricao": "Impressões personalizadas em resina ou filamento para miniaturas, peças de jogo e protótipos exclusivos.",
            "exemplos": "Miniaturas de RPG, acessórios de boardgame, peças de colecionador e componentes decorativos.",
            "preco": "A partir de R$ 180,00 dependendo de tamanho, material e acabamento.",
            "cta": "Solicitar orçamento",
            "badge": "Precisão extrema"
        },
        {
            "titulo": "Modelagem 3D",
            "descricao": "Criação de modelos digitais a partir de referências ou briefing para produção 3D e impressão perfeita.",
            "exemplos": "Personagens personalizados, bustos temáticos, conceitos para jogos e peças exclusivas.",
            "preco": "Orçamento a partir de R$ 250,00 por projeto, com entrega de arquivo pronto para impressão.",
            "cta": "Solicitar orçamento",
            "badge": "Design pronto para impressão"
        },
        {
            "titulo": "Pintura artística",
            "descricao": "Acabamento manual premium com pintura realista, sombreado e texturização em peças impressas.",
            "exemplos": "Figuras de RPG, dioramas, miniaturas de colecionador e objetos decorativos.",
            "preco": "A partir de R$ 120,00 por peça, válido para modelos de até 15cm.",
            "cta": "Solicitar orçamento",
            "badge": "Acabamento de galeria"
        },
        {
            "titulo": "Projetos personalizados",
            "descricao": "Projetos completos para RPG, dioramas, bases temáticas e acessórios customizados sob medida.",
            "exemplos": "Cenários modulares, peças narrativas para RPG, dioramas de batalha e coleções temáticas.",
            "preco": "Base a partir de R$ 320,00, com cotação conforme escopo e complexidade.",
            "cta": "Solicitar orçamento",
            "badge": "Projetos únicos"
        }
    ]
    etapas = [
        {
            "numero": "1",
            "titulo": "Briefing detalhado",
            "descricao": "Você envia referências, objetivos e uso final. Nós revisamos o melhor fluxo para o projeto."
        },
        {
            "numero": "2",
            "titulo": "Modelagem & protótipo",
            "descricao": "Montamos o arquivo 3D ou adaptamos o modelo para impressão com foco em detalhe e resistência."
        },
        {
            "numero": "3",
            "titulo": "Impressão & acabamento",
            "descricao": "Imprimimos, retiramos suportes e aplicamos acabamento, texturas e pintura artística quando necessário."
        },
        {
            "numero": "4",
            "titulo": "Entrega ou envio",
            "descricao": "Receba sua peça pronta para exibição ou jogo, com embalagem segura e orientações de uso."
        }
    ]
    return templates.TemplateResponse("servicos.html", {
        "request": request,
        "titulo": "Serviços",
        "servicos": servicos,
        "etapas": etapas,
        "user": None,
        "is_admin": False,
        "year": datetime.utcnow().year,
    })