from typing import Annotated, Optional
from fastapi import APIRouter, Request, Depends, HTTPException, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from uuid import uuid4
import app.dependencies as dependencies
from app.repositories.produto import ProdutoRepository
from app.repositories.orcamento import OrcamentoRepository
from app.repositories.pergunta import PerguntaRepository
from app.repositories.imagem_produto import ImagemProdutoRepository
from app.models.produto import ProdutoCriarAtualizar
from app.models.imagem_produto import ImagemProdutoCriarAtualizar
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["Admin Panel"])
templates = Jinja2Templates(directory="app/templates")

async def ensure_admin(request: Request):
    """Dependência para garantir que apenas administradores acessem as rotas."""
    user = getattr(request.state, "user", None)
    if not user:
        # Lançar exceção interrompe a execução da rota imediatamente
        raise HTTPException(status_code=401)
    
    if not getattr(request.state, "is_admin", False):
        raise HTTPException(status_code=403, detail="Acesso proibido: Requer privilégios de administrador.")
    return True

@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    _auth: Annotated[bool, Depends(ensure_admin)],
    produto_repo: Annotated[ProdutoRepository, Depends(dependencies.get_produto_repository)],
    orcamento_repo: Annotated[OrcamentoRepository, Depends(dependencies.get_orcamento_repository)],
    pergunta_repo: Annotated[PerguntaRepository, Depends(dependencies.get_pergunta_repository)]
):
    # Coleta de métricas básicas para o Dashboard
    produtos = await produto_repo.listar_produtos()
    orcamentos = await orcamento_repo.listar_orcamentos()
    perguntas = await pergunta_repo.listar_perguntas()
    
    # Filtros simples de status (baseado nos modelos existentes)
    perguntas_pendentes = [p for p in perguntas if p.id_resposta is None]
    
    # O modelo de orçamento atual não tem status explícito no banco, 
    # mas podemos contar o total para o overview
    
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "titulo": "Dashboard Admin | Crimson Claw",
        "user": request.state.user,
        "stats": {
            "total_produtos": len(produtos),
            "total_orcamentos": len(orcamentos),
            "perguntas_pendentes": len(perguntas_pendentes)
        },
        "year": datetime.utcnow().year,
    })

@router.get("/produtos", response_class=HTMLResponse)
async def admin_listar_produtos(
    request: Request,
    _auth: Annotated[bool, Depends(ensure_admin)],
    produto_repo: Annotated[ProdutoRepository, Depends(dependencies.get_produto_repository)],
    categoria_repo: Annotated[dependencies.CategoriaRepository, Depends(dependencies.get_categoria_repository)]
):
    produtos = await produto_repo.listar_produtos()
    categorias = await categoria_repo.listar_categorias()
    
    # Mapeamento para exibir o nome da categoria na tabela
    cat_map = {c.id_categoria: c.nome_categoria for c in categorias}

    return templates.TemplateResponse("admin/produtos_lista.html", {
        "request": request,
        "titulo": "Gerenciar Produtos | Crimson Claw",
        "user": request.state.user,
        "produtos": produtos,
        "cat_map": cat_map,
        "year": datetime.utcnow().year,
    })

@router.post("/produtos/excluir/{produto_id}")
async def admin_excluir_produto(
    produto_id: int,
    _auth: Annotated[bool, Depends(ensure_admin)],
    produto_repo: Annotated[ProdutoRepository, Depends(dependencies.get_produto_repository)]
):
    await produto_repo.delete_produto(produto_id)
    return RedirectResponse(url="/admin/produtos", status_code=303)

@router.get("/produtos/novo", response_class=HTMLResponse)
async def admin_novo_produto_form(
    request: Request,
    _auth: Annotated[bool, Depends(ensure_admin)],
    categoria_repo: Annotated[dependencies.CategoriaRepository, Depends(dependencies.get_categoria_repository)]
):
    categorias = await categoria_repo.listar_categorias()
    return templates.TemplateResponse("admin/produto_form.html", {
        "request": request,
        "titulo": "Novo Produto | Crimson Claw",
        "user": request.state.user,
        "categorias": categorias,
        "produto": None,  # Usado para diferenciar de "editar"
        "year": datetime.utcnow().year,
    })

@router.post("/produtos/novo")
async def admin_criar_produto(
    request: Request,
    _auth: Annotated[bool, Depends(ensure_admin)],
    produto_repo: Annotated[ProdutoRepository, Depends(dependencies.get_produto_repository)],
    imagem_repo: Annotated[ImagemProdutoRepository, Depends(dependencies.get_imagem_produto_repository)],
    nome_produto: str = Form(...),
    descricao: str = Form(...),
    material: str = Form(...),
    altura: float = Form(...),
    comprimento: float = Form(...),
    largura: float = Form(...),
    quantidade: int = Form(...),
    peso: float = Form(...),
    valor: float = Form(...),
    id_categoria: int = Form(...),
    imagem_arquivo: Optional[UploadFile] = File(None)
):
    from app.services.produto_service import ProdutoService
    service = ProdutoService(produto_repo, imagem_repo)
    
    dados_produto = ProdutoCriarAtualizar(
        nome_produto=nome_produto, descricao=descricao, material=material,
        altura=altura, comprimento=comprimento, largura=largura,
        quantidade=quantidade, peso=peso, valor=valor, id_categoria=id_categoria
    )
    
    produto, erro = await service.cadastrar_produto(dados_produto, imagem_arquivo)

    if erro:
        categoria_repo = dependencies.get_categoria_repository(dependencies.get_database())
        categorias = await categoria_repo.listar_categorias()
        return templates.TemplateResponse("admin/produto_form.html", {
            "request": request, "user": request.state.user, "categorias": categorias,
            "error": erro, "year": datetime.utcnow().year,
        })

    return RedirectResponse(url="/admin/produtos", status_code=303)