# Sistema de Email e Confirmação de Cadastro

## Visão Geral

Este projeto implementa um sistema SMTP para envio de emails e um fluxo de confirmação de email para novos usuários. O sistema valida o email do usuário após o cadastro antes que ele possa fazer login.

## Arquitetura

### Componentes Principais

1. **EmailService** (`app/services/email_service.py`)
   - Serviço responsável por enviar emails via SMTP
   - Suporta HTML e texto simples
   - Configurável via variáveis de ambiente

2. **ConfirmacaoEmailService** (`app/services/confirmacao_email_service.py`)
   - Gerencia tokens de confirmação de email
   - Armazena tokens com hash SHA256 para segurança
   - Tokens expiram após 24 horas
   - Valida e marca emails como confirmados

3. **Banco de Dados**
   - Tabela `confirmacao_email` criada em ambos os bancos (SQLite e PostgreSQL)
   - Armazena tokens com hash, email, usuário e status de confirmação

### Fluxo de Confirmação

```
1. Usuário cadastra-se
   ↓
2. Sistema cria token de confirmação
   ↓
3. Email de confirmação é enviado
   ↓
4. Usuário clica no link de confirmação
   ↓
5. Sistema valida e marca email como confirmado
   ↓
6. Usuário pode fazer login
```

## Configuração

### Variáveis de Ambiente

Adicione ao arquivo `.env`:

```env
# SMTP Configuration
SMTP_SERVER=smtp.gmail.com          # Servidor SMTP (exemplo: Gmail)
SMTP_PORT=587                       # Porta SMTP (587 para TLS)
SENDER_EMAIL=seu-email@gmail.com    # Email de envio
SENDER_PASSWORD=sua-senha-app       # Senha ou app-specific password
```

### Para Gmail

1. Ative autenticação de dois fatores
2. Gere uma "App Password" em https://myaccount.google.com/apppasswords
3. Use a senha de app gerada no lugar de sua senha regular

### Para Outros Provedores

Ajuste `SMTP_SERVER` e `SMTP_PORT` conforme o provedor:

- **Outlook**: `smtp-mail.outlook.com`, porta `587`
- **Yahoo**: `smtp.mail.yahoo.com`, porta `587`
- **Gmail**: `smtp.gmail.com`, porta `587`
- **Seu servidor SMTP customizado**: ajuste conforme necessário

## Uso

### Enviar Email

```python
from app.services.email_service import EmailService

service = EmailService()

html_content = "<h1>Bem-vindo!</h1><p>Obrigado por se registrar.</p>"
text_content = "Bem-vindo! Obrigado por se registrar."

enviado = await service.enviar_email(
    "usuario@example.com",
    "Bem-vindo ao Crimson Claw Studio",
    html_content,
    text_content
)
```

### Gerenciar Confirmação de Email

```python
from app.services.confirmacao_email_service import ConfirmacaoEmailService
from app.database.local import Database

db = Database()
confirmacao_service = ConfirmacaoEmailService(db)

# Criar token
token = confirmacao_service.criar_token_confirmacao(
    email="usuario@example.com",
    usuario_id=1
)

# Enviar email de confirmação
enviado = await confirmacao_service.enviar_email_confirmacao(
    email="usuario@example.com",
    nome="João",
    token=token,
    url_base="http://localhost:8000"
)

# Verificar token e confirmar
resultado = confirmacao_service.verificar_token(token)
if resultado:
    confirmacao_service.marcar_como_confirmado(resultado["token_hash"])
```

## Rotas HTTP

### GET `/confirmar-email?token=<token>`

Confirma o email do usuário.

**Respostas:**
- `200 OK`: Email confirmado com sucesso
- `200 OK` com mensagem de erro: Token inválido ou expirado

### POST `/cadastro`

Cadastra novo usuário e envia email de confirmação.

**Form Data:**
- `nome`: Nome do usuário
- `email`: Email do usuário
- `senha`: Senha
- `cpf`: CPF

**Respostas:**
- Email de confirmação enviado se SMTP estiver configurado
- Usuário pode fazer login mesmo sem confirmar (opcional, configurable)

## Testes

Execute os testes de confirmação de email:

```bash
python -m pytest tests/test_confirmacao_email.py -v
```

Testes incluem:

- ✓ Criar token de confirmação
- ✓ Verificar token válido
- ✓ Rejeitar token inválido
- ✓ Marcar email como confirmado
- ✓ Expiração de token
- ✓ Múltiplos usuários com tokens diferentes

## Segurança

- **Tokens com Hash**: Os tokens são armazenados com hash SHA256 no banco de dados
- **Expiração**: Tokens expiram após 24 horas
- **Único**: `token_hash` possui constraint UNIQUE no banco de dados
- **Aleatoriedade**: Tokens gerados com `secrets.token_urlsafe(32)`

## Troubleshooting

### Email não é enviado

1. Verifique se `SMTP_SERVER`, `SENDER_EMAIL` e `SENDER_PASSWORD` estão configurados
2. Verifique a conexão com o servidor SMTP
3. Teste com um script Python simples para validar credenciais
4. Verifique permissões de firewall para porta SMTP

### Token inválido ao confirmar

1. Verifique se o token não expirou (24 horas)
2. Certifique-se de que está usando a URL correta
3. Verifique se o banco de dados está sincronizado

### Múltiplos emails enviados

Verifique se há múltiplas chamadas para `criar_token_confirmacao()` no fluxo de cadastro.

## Próximos Passos

- [ ] Implementar reenvio de email de confirmação
- [ ] Adicionar confirmação de email obrigatória para login
- [ ] Implementar notificações por email (pedidos, status, etc)
- [ ] Adicionar template de email customizável
- [ ] Implementar filas de email (Celery/RQ)
