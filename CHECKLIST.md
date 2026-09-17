# Crimson Claw Studio — Estado do Projeto

**Stack**: FastAPI + Jinja2 + PostgreSQL (Docker) + SQLite (dev)
**Comando dev**: `uvicorn app.main:app --reload` (rodar da raiz)
**Container DB**: `docker run --name crimson-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=crimson_db -p 5432:5432 -d postgres`

---

## Backend

### Autenticação e Usuários
- [x] Cadastro com validação via `UsuarioService`
- [x] Login com `LoginAttemptService` — bloqueio após tentativas falhas
- [x] Sessão via `SessionMiddleware` (cookie `crimson_session`)
- [x] Middleware `SessionUserMiddleware` — injeta `request.state.user` em todas as rotas
- [x] Middleware `DocsAuthMiddleware` — protege `/docs` e `/redoc`
- [x] Logout com limpeza de sessão
- [x] Confirmação de email com token SHA256 + expiração 24h (`ConfirmacaoEmailService`)
- [x] Reenvio de email de confirmação
- [x] Redirecionamento pós-login para URL de origem (`next` na sessão)
- [ ] Confirmação de email obrigatória para login (token gerado, verificação não bloqueante ainda)
- [ ] Hash de senha (atualmente armazenada em texto plano)
- [ ] Recuperação de senha (esqueci minha senha)

### Produtos e Catálogo
- [x] Listagem de produtos com filtros (categoria, preço mín/máx)
- [x] Detalhe do produto com imagens e avaliações
- [x] Upload de imagens via admin (`ProdutoService`)
- [x] Favoritar/desfavoritar produto (toggle)
- [x] Avaliação de produto (1–5 estrelas + comentário, uma por usuário)
- [ ] Estoque / controle de quantidade disponível
- [ ] Variações reais de produto no banco (tamanho, material, pintura estão hardcoded no template)
- [ ] Paginação na listagem de produtos

### Carrinho e Pedidos
- [x] Carrinho em sessão (adicionar, remover, visualizar)
- [x] Sugestões no carrinho (baseadas em favoritos ou categoria)
- [x] Finalização envia email ao admin + registra mensagem no banco
- [ ] Pedido real no banco (tabela `pedido` existe mas não é usada no checkout)
- [ ] Integração com pagamento
- [ ] Status de pedido visível na conta do usuário (lista retorna `[]` atualmente)
- [ ] Notificação de status por email

### Orçamento
- [x] Formulário de orçamento com upload de arquivo (STL, OBJ, 3MF, imagem, PDF — máx 20MB)
- [x] Validação de extensão e tamanho
- [x] Persistência no banco via `OrcamentoRepository`
- [ ] Orçamentos visíveis na conta do usuário (lista retorna `[]` atualmente)
- [ ] Resposta do admin ao orçamento com notificação por email

### Admin
- [x] Dashboard com métricas (total produtos, orçamentos, perguntas pendentes)
- [x] Listagem e exclusão de produtos
- [x] Criação de produto com upload de imagens
- [x] Listagem, exclusão e toggle de destaque em avaliações
- [x] Proteção de rotas admin via `ensure_admin` (401/403)
- [ ] Edição de produto existente
- [ ] Gestão de orçamentos (visualizar, responder, mudar status)
- [ ] Gestão de pedidos (visualizar, atualizar status)
- [ ] Gestão de usuários (listar, bloquear, promover a admin)
- [ ] Gestão de categorias (criar, editar, excluir)

### API REST
- [x] Routers organizados em `app/routers/api/` para todas as entidades
- [ ] Autenticação JWT nas rotas de API (atualmente sem proteção)
- [ ] Documentação OpenAPI revisada e completa

---

## Frontend

### Semântica e Acessibilidade
- [x] `<ol>/<li>` corretos em `home.html` (steps)
- [x] `<article>` + `aria-labelledby` em `servicos.html` (process-cards)
- [x] `<figure>/<blockquote>/<figcaption>` em depoimentos (`sobre.html`, `home.html`)
- [x] `<figure>/<figcaption>/<blockquote>` em avaliações (`product.html`)
- [x] Schema.org `Product` + `AggregateRating` + `Review` em `product.html`

### Mobile-First
- [x] Navbar reescrita mobile-first (toggle hambúrguer, expande em ≥840px)
- [x] `cart.css` — `.cart-grid`, `.cart-item` mobile-first
- [x] `account.css` — `.account-layout`, `.favorite-card`, `.field-grid` mobile-first
- [x] `products.css` — filtros e thumbnails mobile-first
- [x] `home.css` — `.home-hero`, `.home-cta__card` mobile-first
- [x] `style.css` — `.quote-grid`, `.card` mobile-first
- [x] `orcamento.css` — `.quote-form__row` mobile-first
- [x] `touch-action: manipulation` em `.carousel-btn` e `.faq-item summary`

### Medidas CSS
- [x] `px → rem` no carousel (`home.css`)
- [x] `px → rem` no `filters-bar` (`products.css`)
- [x] `px → rem` no `small` (`style.css`)
- [x] `vh → dvh` com fallback em `body` e `.login-page` (`style.css`)
- [x] `clamp()` em `.home-hero h1`, `.price`, `.faq-hero h1`, `.account-header h1`

### Galeria de Produto
- [x] PhotoSwipe 5 via CDN — zoom, swipe, teclado, setas
- [x] Miniaturas trocam imagem principal e sincronizam índice do lightbox
- [x] `cursor: zoom-in` na imagem principal
- [ ] Dimensões reais das imagens salvas no banco para o PhotoSwipe (atualmente fixo 1200×1200)

---

## Infraestrutura

### Banco de Dados
- [x] PostgreSQL via Docker (`crimson-postgres`)
- [x] SQLite para desenvolvimento local
- [x] Schema em `postgres_schema.sql`
- [x] Migrations automáticas no `start_database()`
- [ ] Migrations versionadas (Alembic)

### Backups
- [x] `backup_db.bat` — `pg_dump` dentro do container, retenção 7 dias
- [x] `backup_imagens.bat` — `Compress-Archive` de `app/static/uploads`, retenção 7 dias

### Deploy
- [ ] `Dockerfile` e `docker-compose.yml` (arquivos existem mas estão vazios)
- [ ] Variáveis de ambiente configuradas no servidor (ver `.env.example`)
- [ ] HTTPS / certificado SSL
- [ ] SPF/DKIM/DMARC para entregabilidade de email
- [ ] Configurar `WORKERS` para produção (uvicorn multiprocess)
- [ ] Monitoramento / health check além do `/health` atual

---

## Testes

- [x] `test_auth.py` — 6 testes (cadastro, login, validações)
- [x] `test_confirmacao_email.py` — 8 testes (token, expiração, múltiplos usuários)
- [x] `test_product_service.py` — 5 testes (CRUD, categorias)
- [x] `test_login_attempt_service.py` — 4 testes (bloqueio, reset, duração)
- [x] **Total: 23 testes passando**
- [ ] Testes para `cart_service`
- [ ] Testes para `orcamento` (upload, validação de extensão)
- [ ] Testes de integração para rotas web (com cliente HTTP)
- [ ] Cobertura de código (pytest-cov)

---

## Próximos Passos — Para Análise

Os itens abaixo estão ordenados por impacto no produto final. Analise e decida a prioridade.

### 🔴 Alta prioridade — afeta funcionamento core

1. **Hash de senha**
   Senhas estão em texto plano no banco. Implementar `bcrypt` ou `passlib` no `UsuarioService` antes de qualquer deploy.

2. **Pedido real no checkout**
   O carrinho finaliza enviando email, mas não cria registro na tabela `pedido`. O usuário não tem histórico de compras. Conectar `carrinho_finalizar` ao `PedidoRepository`.

3. **Variações de produto no banco**
   Tamanho, material e pintura estão hardcoded no template. Criar tabela de variações ou campo JSON no produto para que o admin controle as opções.

4. **Dockerfile e docker-compose**
   Arquivos existem mas estão vazios. Necessário para qualquer deploy ou ambiente compartilhado.

### 🟡 Média prioridade — melhora experiência

5. **Confirmação de email obrigatória para login**
   Token já é gerado no cadastro. Falta bloquear o login de usuários não confirmados e exibir mensagem orientando a confirmar.

6. **Edição de produto no admin**
   Criação e exclusão existem, mas não há rota de edição. Reaproveitar `produto_form.html` com dados pré-preenchidos.

7. **Orçamentos e pedidos na conta do usuário**
   As listas retornam `[]` atualmente. Conectar `OrcamentoRepository` e `PedidoRepository` na rota `/minha-conta`.

8. **Dimensões reais das imagens para o PhotoSwipe**
   Salvar `width` e `height` no upload de imagem para o zoom funcionar corretamente em todos os formatos.

9. **Paginação na listagem de produtos**
   Sem paginação, todos os produtos são carregados de uma vez. Implementar `limit/offset` no `ProdutoRepository`.

### 🟢 Baixa prioridade — qualidade e escala

10. **JWT nas rotas de API**
    As rotas em `/api/` não têm autenticação. Necessário se a API for consumida por clientes externos ou mobile.

11. **Migrations com Alembic**
    Migrations automáticas funcionam para dev, mas em produção é arriscado. Alembic dá controle de versão do schema.

12. **Testes de carrinho e orçamento**
    As partes mais críticas do fluxo de negócio não têm cobertura de teste.

13. **Gestão de usuários no admin**
    Listar usuários, bloquear contas e promover a admin são funcionalidades esperadas num painel administrativo.

14. **Recuperação de senha**
    Fluxo "esqueci minha senha" com token por email, similar ao já implementado para confirmação de email.

---

**Última atualização**: estado atual do projeto após sessões de desenvolvimento
**Testes**: 23 passando
**Status geral**: Em desenvolvimento ativo
