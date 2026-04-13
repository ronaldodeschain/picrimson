from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


from app.routers.api import usuario, categoria, produto, pedido, pagamento, servico, endereco, telefone, avaliacao, caixa, carrinho, cupom, email, entrega, favoritos, imagem_produto, item_pedido, mensagem, nota_fiscal, orcamento, rastreio, pergunta, resposta

templates = Jinja2Templates(directory="app/templates")

app = FastAPI(
    title = "Crimson Claw Studio",
    description = "Backend para Projeto Integrador",
    version = "1.0.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

api_prefix = "/api"
app.include_router(usuario.router, prefix=api_prefix)
app.include_router(categoria.router, prefix=api_prefix)
app.include_router(produto.router, prefix=api_prefix)
app.include_router(pedido.router, prefix=api_prefix)
app.include_router(pagamento.router, prefix=api_prefix)
app.include_router(servico.router, prefix=api_prefix)
app.include_router(endereco.router, prefix=api_prefix)
app.include_router(telefone.router, prefix=api_prefix)
app.include_router(avaliacao.router, prefix=api_prefix)
app.include_router(caixa.router, prefix=api_prefix)
app.include_router(carrinho.router, prefix=api_prefix)
app.include_router(cupom.router, prefix=api_prefix)
app.include_router(email.router, prefix=api_prefix)
app.include_router(entrega.router, prefix=api_prefix)
app.include_router(favoritos.router, prefix=api_prefix)
app.include_router(imagem_produto.router, prefix=api_prefix)
app.include_router(item_pedido.router, prefix=api_prefix)
app.include_router(mensagem.router, prefix=api_prefix)
app.include_router(nota_fiscal.router, prefix=api_prefix)
app.include_router(orcamento.router, prefix=api_prefix)
app.include_router(rastreio.router, prefix=api_prefix)
app.include_router(pergunta.router, prefix=api_prefix)
app.include_router(resposta.router, prefix=api_prefix)


@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/",response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse("home.html",{
        "request": request,
        "titulo": "Crimson Claw Studio",
        "versão": "1.0.0",
        "user": None,
        "is_admin": False,
        "year": datetime.utcnow().year,
    })

@app.get("/login.html",response_class=HTMLResponse)
async def login(request:Request):
    return templates.TemplateResponse("login.html",{
        "request": request,
        "user":None,
        "is_admin": False,
        "is_auth":True,
        "year": datetime.utcnow().year,
    })