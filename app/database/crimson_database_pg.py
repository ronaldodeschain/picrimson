import psycopg2
import os
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(
        self,
        dbname="crimson_db",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    ):
        self.dbname = os.getenv("DB_NAME", dbname)
        self.user = os.getenv("DB_USER", user)
        self.password = os.getenv("DB_PASS", password)
        self.host = os.getenv("DB_HOST", host)
        self.port = os.getenv("DB_PORT", port)
        self.database_url = os.getenv("DATABASE_URL")
        self.start_database()

    @contextmanager
    def connect(self):
        if self.database_url:
            connection = psycopg2.connect(self.database_url)
        else:
            connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            
        try:
            yield connection
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()

    def start_database(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id_usuario SERIAL PRIMARY KEY,
                    nome_usuario TEXT,
                    login TEXT,
                    senha TEXT,
                    cpf TEXT,
                    id_favoritos INTEGER,
                    id_email INTEGER,
                    id_endereco INTEGER,
                    id_carrinho INTEGER,
                    id_telefone INTEGER,
                    id_mensagem INTEGER,
                    id_avaliacoes INTEGER,
                    id_pergunta INTEGER,
                    id_resposta INTEGER,
                    role TEXT DEFAULT 'user'
                );

                CREATE TABLE IF NOT EXISTS categorias (
                    id_categoria SERIAL PRIMARY KEY,
                    nome_categoria TEXT,
                    id_produto INTEGER
                );

                CREATE TABLE IF NOT EXISTS produtos (
                    id_produto SERIAL PRIMARY KEY,
                    nome_produto TEXT,
                    descricao TEXT,
                    material TEXT,
                    altura REAL,
                    comprimento REAL,
                    largura REAL,
                    quantidade INTEGER,
                    peso REAL,
                    valor REAL,
                    id_item_pedidos INTEGER,
                    id_categoria INTEGER,
                    id_avaliacoes INTEGER,
                    id_imagem_produto INTEGER,
                    id_favoritos INTEGER,
                    id_pergunta INTEGER,
                    id_resposta INTEGER
                );

                CREATE TABLE IF NOT EXISTS imagem_produtos (
                    id_imagem_produto SERIAL PRIMARY KEY,
                    nome_imagem TEXT,
                    arquivo_imagem TEXT,
                    id_produto INTEGER
                );

                CREATE TABLE IF NOT EXISTS item_pedidos (
                    id_item_pedido SERIAL PRIMARY KEY,
                    id_usuario INTEGER,
                    id_produto INTEGER,
                    id_carrinho INTEGER
                );

                CREATE TABLE IF NOT EXISTS notas_fiscais (
                    id_nota_fiscal SERIAL PRIMARY KEY,
                    forma_pagamento TEXT,
                    data_emissao TEXT,
                    serie TEXT,
                    numero INTEGER,
                    status TEXT,
                    valor_total REAL,
                    id_caixa INTEGER,
                    id_pagamento INTEGER,
                    id_mensagem INTEGER
                );

                CREATE TABLE IF NOT EXISTS enderecos (
                    id_endereco SERIAL PRIMARY KEY,
                    rua TEXT,
                    numero INTEGER,
                    complemento TEXT,
                    cep TEXT,
                    cidade TEXT,
                    estado TEXT,
                    observacoes TEXT,
                    id_usuario INTEGER
                );

                CREATE TABLE IF NOT EXISTS orcamentos (
                    id_orcamento SERIAL PRIMARY KEY,
                    mensagem TEXT,
                    arquivo TEXT,
                    imagem TEXT,
                    id_mensagem INTEGER,
                    id_servico INTEGER
                    , nome TEXT
                    , contato TEXT
                    , tipo_projeto TEXT
                    , descricao TEXT
                    , tamanho_desejado TEXT
                );

                CREATE TABLE IF NOT EXISTS avaliacoes (
                    id_avaliacao SERIAL PRIMARY KEY,
                    comentario TEXT,
                    avaliacao REAL,
                    id_produto INTEGER,
                    id_usuario INTEGER
                );

                CREATE TABLE IF NOT EXISTS pagamentos (
                    id_pagamento SERIAL PRIMARY KEY,
                    expiracao TEXT,
                    valor_total REAL,
                    data_pagamento TEXT,
                    status_pagamento TEXT,
                    pixTxid TEXT,
                    id_pedido INTEGER,
                    id_caixa INTEGER,
                    id_nota_fiscal INTEGER,
                    id_entrega INTEGER
                );

                CREATE TABLE IF NOT EXISTS pedidos (
                    id_pedido SERIAL PRIMARY KEY,
                    valor_total REAL,
                    observacoes TEXT,
                    id_pagamento INTEGER,
                    id_carrinho INTEGER,
                    id_cupom INTEGER,
                    id_servico INTEGER
                );

                CREATE TABLE IF NOT EXISTS cupons (
                    id_cupom SERIAL PRIMARY KEY,
                    chave_cupom TEXT,
                    valor_cupom REAL,
                    tipo_cupom TEXT,
                    id_pedido INTEGER
                );

                CREATE TABLE IF NOT EXISTS rastreio (
                    id_rastreio SERIAL PRIMARY KEY,
                    codigo_rastreio INTEGER,
                    id_entrega INTEGER,
                    id_mensagem INTEGER
                );

                CREATE TABLE IF NOT EXISTS caixa (
                    id_caixa SERIAL PRIMARY KEY,
                    tipo_movimentacao TEXT,
                    valor REAL,
                    descricao TEXT,
                    data_movimentacao TEXT,
                    id_nota_fiscal INTEGER,
                    id_pagamento INTEGER
                );

                CREATE TABLE IF NOT EXISTS email (
                    id_email SERIAL PRIMARY KEY,
                    email TEXT,
                    id_usuario INTEGER
                );

                CREATE TABLE IF NOT EXISTS carrinho (
                    id_carrinho SERIAL PRIMARY KEY,
                    id_servico INTEGER,
                    id_pedido INTEGER,
                    id_item_pedido INTEGER,
                    id_usuario INTEGER
                );

                CREATE TABLE IF NOT EXISTS servico (
                    id_servico SERIAL PRIMARY KEY,
                    tipo_servico TEXT,
                    valor_servico REAL,
                    descricao TEXT,
                    id_pedido INTEGER,
                    id_orcamento INTEGER
                );

                CREATE TABLE IF NOT EXISTS mensagem (
                    id_mensagem SERIAL PRIMARY KEY,
                    mensagem TEXT,
                    tipo_mensagem TEXT,
                    id_pedido INTEGER,
                    id_email INTEGER,
                    id_orcamento INTEGER,
                    id_usuario INTEGER,
                    id_nota_fiscal INTEGER,
                    id_rastreio INTEGER
                );

                CREATE TABLE IF NOT EXISTS telefone (
                    id_telefone SERIAL PRIMARY KEY,
                    telefone_principal INTEGER,
                    telefone_secundario INTEGER,
                    id_usuario INTEGER
                );

                CREATE TABLE IF NOT EXISTS favoritos (
                    id_favoritos SERIAL PRIMARY KEY,
                    id_produto INTEGER,
                    id_usuario INTEGER
                );

                CREATE TABLE IF NOT EXISTS entrega (
                    id_entrega SERIAL PRIMARY KEY,
                    mensagem TEXT,
                    tipo_mensagem TEXT,
                    data_entrega_prevista TEXT,
                    data_envio TEXT,
                    tipo_entrega TEXT,
                    endereco_entrega TEXT,
                    observacoes TEXT,
                    data_pedido TEXT,
                    status_entrega TEXT,
                    id_pedido INTEGER,
                    id_rastreio INTEGER
                );

                CREATE TABLE IF NOT EXISTS pergunta (
                    id_pergunta SERIAL PRIMARY KEY,
                    pergunta TEXT,
                    data_criacao TEXT,
                    id_usuario INTEGER,
                    id_produto INTEGER,
                    id_resposta INTEGER
                );

                CREATE TABLE IF NOT EXISTS resposta (
                    id_resposta SERIAL PRIMARY KEY,
                    texto_resposta TEXT,
                    data_resposta TEXT,
                    id_usuario INTEGER,
                    id_produto INTEGER,
                    id_pergunta INTEGER
                );
            """)
        print("Banco de dados PostgreSQL criado com sucesso!")