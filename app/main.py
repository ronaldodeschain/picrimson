from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


from app.routers import usuario, categoria, produto, pedido, pagamento, servico, endereco, telefone, avaliacao, caixa, carrinho, cupom, email, entrega, favoritos, imagem_produto, item_pedido, mensagem, nota_fiscal, orcamento, rastreio

templates = Jinja2Templates(directory="app/templates")

app = FastAPI(
    title = "Crimson Claw Studio",
    description = "Backend para Projeto Integrador",
    version = "1.0.0"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(usuario.router)
app.include_router(categoria.router)
app.include_router(produto.router)
app.include_router(pedido.router)
app.include_router(pagamento.router)
app.include_router(servico.router)
app.include_router(endereco.router)
app.include_router(telefone.router)
app.include_router(avaliacao.router)
app.include_router(caixa.router)
app.include_router(carrinho.router)
app.include_router(cupom.router)
app.include_router(email.router)
app.include_router(entrega.router)
app.include_router(favoritos.router)
app.include_router(imagem_produto.router)
app.include_router(item_pedido.router)
app.include_router(mensagem.router)
app.include_router(nota_fiscal.router)
app.include_router(orcamento.router)
app.include_router(rastreio.router)


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