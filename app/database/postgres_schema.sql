-- PostgreSQL schema for the services (all tables converted from SQLite)

-- Table: usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nome_usuario VARCHAR(255),
    login VARCHAR(255),
    senha VARCHAR(255),
    cpf VARCHAR(14),
    id_favoritos INTEGER REFERENCES favoritos(id_favoritos),
    id_email INTEGER REFERENCES email(id_email),
    id_endereco INTEGER REFERENCES enderecos(id_endereco),
    id_carrinho INTEGER REFERENCES carrinho(id_carrinho),
    id_telefone INTEGER REFERENCES telefone(id_telefone),
    id_mensagem INTEGER REFERENCES mensagem(id_mensagem),
    id_avaliacoes INTEGER REFERENCES avaliacoes(id_avaliacao),
    id_pergunta INTEGER REFERENCES pergunta(id_pergunta),
    id_resposta INTEGER REFERENCES resposta(id_resposta),
    role VARCHAR(50) DEFAULT 'user'
);

-- Table: categorias
CREATE TABLE IF NOT EXISTS categorias (
    id_categoria SERIAL PRIMARY KEY,
    nome_categoria VARCHAR(255),
    id_produto INTEGER REFERENCES produtos(id_produto)
);

-- Table: produtos
CREATE TABLE IF NOT EXISTS produtos (
    id_produto SERIAL PRIMARY KEY,
    nome_produto VARCHAR(255),
    descricao TEXT,
    material VARCHAR(255),
    altura REAL,
    comprimento REAL,
    largura REAL,
    quantidade INTEGER,
    peso REAL,
    valor REAL,
    id_item_pedidos INTEGER REFERENCES item_pedidos(id_item_pedido),
    id_categoria INTEGER REFERENCES categorias(id_categoria),
    id_avaliacoes INTEGER REFERENCES avaliacoes(id_avaliacao),
    id_imagem_produto INTEGER REFERENCES imagem_produtos(id_imagem_produto),
    id_favoritos INTEGER REFERENCES favoritos(id_favoritos),
    id_pergunta INTEGER REFERENCES pergunta(id_pergunta),
    id_resposta INTEGER REFERENCES resposta(id_resposta)
);

-- Table: imagem_produtos
CREATE TABLE IF NOT EXISTS imagem_produtos (
    id_imagem_produto SERIAL PRIMARY KEY,
    nome_imagem VARCHAR(255),
    arquivo_imagem TEXT,
    id_produto INTEGER REFERENCES produtos(id_produto)
);

-- Table: item_pedidos
CREATE TABLE IF NOT EXISTS item_pedidos (
    id_item_pedido SERIAL PRIMARY KEY,
    id_usuario INTEGER REFERENCES usuarios(id_usuario),
    id_produto INTEGER REFERENCES produtos(id_produto),
    id_carrinho INTEGER REFERENCES carrinho(id_carrinho)
);

-- Table: notas_fiscais
CREATE TABLE IF NOT EXISTS notas_fiscais (
    id_nota_fiscal SERIAL PRIMARY KEY,
    forma_pagamento VARCHAR(255),
    data_emissao DATE,
    serie VARCHAR(255),
    numero INTEGER,
    status VARCHAR(50),
    valor_total REAL,
    id_caixa INTEGER REFERENCES caixa(id_caixa),
    id_pagamento INTEGER REFERENCES pagamentos(id_pagamento),
    id_mensagem INTEGER REFERENCES mensagem(id_mensagem)
);

-- Table: enderecos
CREATE TABLE IF NOT EXISTS enderecos (
    id_endereco SERIAL PRIMARY KEY,
    rua VARCHAR(255),
    numero INTEGER,
    complemento VARCHAR(255),
    cep VARCHAR(10),
    cidade VARCHAR(255),
    estado VARCHAR(2),
    observacoes TEXT,
    id_usuario INTEGER REFERENCES usuarios(id_usuario)
);

-- Table: orcamentos
CREATE TABLE IF NOT EXISTS orcamentos (
    id_orcamento SERIAL PRIMARY KEY,
    mensagem TEXT,
    arquivo VARCHAR(255),
    imagem VARCHAR(255),
    id_mensagem INTEGER REFERENCES mensagem(id_mensagem),
    id_servico INTEGER REFERENCES servico(id_servico)
);

-- Table: avaliacoes
CREATE TABLE IF NOT EXISTS avaliacoes (
    id_avaliacao SERIAL PRIMARY KEY,
    comentario TEXT,
    avaliacao REAL,
    id_produto INTEGER REFERENCES produtos(id_produto),
    id_usuario INTEGER REFERENCES usuarios(id_usuario)
);

-- Table: pagamentos
CREATE TABLE IF NOT EXISTS pagamentos (
    id_pagamento SERIAL PRIMARY KEY,
    expiracao DATE,
    valor_total REAL,
    data_pagamento DATE,
    status_pagamento VARCHAR(50),
    pixTxid VARCHAR(255),
    id_pedido INTEGER REFERENCES pedidos(id_pedido),
    id_caixa INTEGER REFERENCES caixa(id_caixa),
    id_nota_fiscal INTEGER REFERENCES notas_fiscais(id_nota_fiscal),
    id_entrega INTEGER REFERENCES entrega(id_entrega)
);

-- Table: pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido SERIAL PRIMARY KEY,
    valor_total REAL,
    observacoes TEXT,
    id_pagamento INTEGER REFERENCES pagamentos(id_pagamento),
    id_carrinho INTEGER REFERENCES carrinho(id_carrinho),
    id_cupom INTEGER REFERENCES cupons(id_cupom),
    id_servico INTEGER REFERENCES servico(id_servico)
);

-- Table: cupons
CREATE TABLE IF NOT EXISTS cupons (
    id_cupom SERIAL PRIMARY KEY,
    chave_cupom VARCHAR(255),
    valor_cupom REAL,
    tipo_cupom VARCHAR(50),
    id_pedido INTEGER REFERENCES pedidos(id_pedido)
);

-- Table: rastreio
CREATE TABLE IF NOT EXISTS rastreio (
    id_rastreio SERIAL PRIMARY KEY,
    codigo_rastreio INTEGER,
    id_entrega INTEGER REFERENCES entrega(id_entrega),
    id_mensagem INTEGER REFERENCES mensagem(id_mensagem)
);

-- Table: caixa
CREATE TABLE IF NOT EXISTS caixa (
    id_caixa SERIAL PRIMARY KEY,
    tipo_movimentacao VARCHAR(50),
    valor REAL,
    descricao TEXT,
    data_movimentacao DATE,
    id_nota_fiscal INTEGER REFERENCES notas_fiscais(id_nota_fiscal),
    id_pagamento INTEGER REFERENCES pagamentos(id_pagamento)
);

-- Table: email
CREATE TABLE IF NOT EXISTS email (
    id_email SERIAL PRIMARY KEY,
    email VARCHAR(255),
    id_usuario INTEGER REFERENCES usuarios(id_usuario)
);

-- Table: carrinho
CREATE TABLE IF NOT EXISTS carrinho (
    id_carrinho SERIAL PRIMARY KEY,
    id_servico INTEGER REFERENCES servico(id_servico),
    id_pedido INTEGER REFERENCES pedidos(id_pedido),
    id_item_pedido INTEGER REFERENCES item_pedidos(id_item_pedido),
    id_usuario INTEGER REFERENCES usuarios(id_usuario)
);

-- Table: servico
CREATE TABLE IF NOT EXISTS servico (
    id_servico SERIAL PRIMARY KEY,
    tipo_servico VARCHAR(255),
    valor_servico REAL,
    descricao TEXT,
    id_pedido INTEGER REFERENCES pedidos(id_pedido),
    id_orcamento INTEGER REFERENCES orcamentos(id_orcamento)
);

-- Table: mensagem
CREATE TABLE IF NOT EXISTS mensagem (
    id_mensagem SERIAL PRIMARY KEY,
    mensagem TEXT,
    tipo_mensagem VARCHAR(50),
    id_pedido INTEGER REFERENCES pedidos(id_pedido),
    id_email INTEGER REFERENCES email(id_email),
    id_orcamento INTEGER REFERENCES orcamentos(id_orcamento),
    id_usuario INTEGER REFERENCES usuarios(id_usuario),
    id_nota_fiscal INTEGER REFERENCES notas_fiscais(id_nota_fiscal),
    id_rastreio INTEGER REFERENCES rastreio(id_rastreio)
);

-- Table: telefone
CREATE TABLE IF NOT EXISTS telefone (
    id_telefone SERIAL PRIMARY KEY,
    telefone_principal VARCHAR(20),
    telefone_secundario VARCHAR(20),
    id_usuario INTEGER REFERENCES usuarios(id_usuario)
);

-- Table: favoritos
CREATE TABLE IF NOT EXISTS favoritos (
    id_favoritos SERIAL PRIMARY KEY,
    id_produto INTEGER REFERENCES produtos(id_produto),
    id_usuario INTEGER REFERENCES usuarios(id_usuario)
);

-- Table: entrega
CREATE TABLE IF NOT EXISTS entrega (
    id_entrega SERIAL PRIMARY KEY,
    mensagem TEXT,
    tipo_mensagem VARCHAR(50),
    data_entrega_prevista DATE,
    data_envio DATE,
    tipo_entrega VARCHAR(50),
    endereco_entrega TEXT,
    observacoes TEXT,
    data_pedido DATE,
    status_entrega VARCHAR(50),
    id_pedido INTEGER REFERENCES pedidos(id_pedido),
    id_rastreio INTEGER REFERENCES rastreio(id_rastreio)
);

-- Table: pergunta
CREATE TABLE IF NOT EXISTS pergunta (
    id_pergunta SERIAL PRIMARY KEY,
    pergunta TEXT,
    data_criacao DATE,
    id_usuario INTEGER REFERENCES usuarios(id_usuario),
    id_produto INTEGER REFERENCES produtos(id_produto),
    id_resposta INTEGER REFERENCES resposta(id_resposta)
);

-- Table: resposta
CREATE TABLE IF NOT EXISTS resposta (
    id_resposta SERIAL PRIMARY KEY,
    texto_resposta TEXT,
    data_resposta DATE,
    id_usuario INTEGER REFERENCES usuarios(id_usuario),
    id_produto INTEGER REFERENCES produtos(id_produto),
    id_pergunta INTEGER REFERENCES pergunta(id_pergunta)
);