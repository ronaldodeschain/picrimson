import psycopg2
from contextlib import contextmanager
import os

class PostgresDatabase:
    def __init__(self):
        self.url = os.getenv("DATABASE_URL", "postgresql://user_admin:password123@localhost:5432/crimson_db")
        self.start_database()

    @contextmanager
    def connect(self):
        connection = psycopg2.connect(self.url)
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
            with connection.cursor() as cursor:
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

                    -- Script para adicionar a coluna id_pergunta caso ela não exista (Postgres 9.6+)
                    DO $$ 
                    BEGIN 
                        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='resposta' AND column_name='id_pergunta') THEN
                            ALTER TABLE resposta ADD COLUMN id_pergunta INTEGER;
                        END IF;
                    END $$;
                """)
        print("Banco de dados PostgreSQL sincronizado!")