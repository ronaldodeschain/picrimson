import sqlite3
from contextlib import contextmanager

class Database():
    def __init__ (self,nome_arquivo="crimson.db"):
        self.nome_arquivo = nome_arquivo
        self.start_database()
        
    @contextmanager
    def connect(self):
        connection = sqlite3.connect(self.nome_arquivo)
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
            cursor.executescript("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_usuario TEXT,
                    login TEXT,
                    senha TEXT,
                    cpf TEXT
                    , role TEXT DEFAULT 'user'
                );

                CREATE TABLE IF NOT EXISTS categorias (
                    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_categoria TEXT
                );

                CREATE TABLE IF NOT EXISTS produtos (
                    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_produto TEXT,
                    descricao TEXT,
                    material TEXT,
                    altura REAL,
                    comprimento REAL,
                    largura REAL,
                    quantidade INTEGER,
                    peso REAL,
                    valor REAL
                );

                CREATE TABLE IF NOT EXISTS imagem_produtos (
                    id_imagem_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_imagem TEXT,
                    arquivo_imagem TEXT,
                    id_produto INTEGER,
                    FOREIGN KEY(id_produto) REFERENCES produtos(id_produto)
                );

                CREATE TABLE IF NOT EXISTS item_pedidos (
                    id_item_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_usuario INTEGER,
                    id_produto INTEGER,
                    id_carrinho INTEGER,
                    FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario),
                    FOREIGN KEY(id_produto) REFERENCES produtos(id_produto)
                );

                CREATE TABLE IF NOT EXISTS notas_fiscais (
                    id_nota_fiscal INTEGER PRIMARY KEY AUTOINCREMENT,
                    forma_pagamento TEXT,
                    data_emissao TEXT,
                    serie TEXT,
                    numero INTEGER,
                    status TEXT,
                    id_caixa INTEGER,
                    id_pagamento INTEGER,
                    id_mensagem INTEGER
                );

                CREATE TABLE IF NOT EXISTS enderecos (
                    id_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
                    rua TEXT,
                    numero INTEGER,
                    complemento TEXT,
                    cep TEXT,
                    cidade TEXT,
                    estado TEXT,
                    observacoes TEXT,
                    id_usuario INTEGER,
                    FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
                );

                CREATE TABLE IF NOT EXISTS orcamentos (
                    id_orcamento INTEGER PRIMARY KEY AUTOINCREMENT,
                    mensagem TEXT,
                    arquivo TEXT,
                    imagem TEXT,
                    id_mensagem INTEGER,
                    id_servico INTEGER
                );

                CREATE TABLE IF NOT EXISTS avaliacoes (
                    id_avaliacao INTEGER PRIMARY KEY AUTOINCREMENT,
                    comentario TEXT,
                    avaliacao REAL,
                    id_produto INTEGER,
                    id_usuario INTEGER,
                    FOREIGN KEY(id_produto) REFERENCES produtos(id_produto),
                    FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
                );

                CREATE TABLE IF NOT EXISTS pagamentos (
                    id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
                    expiracao TEXT,
                    valor_total REAL,
                    data_pagamento TEXT,
                    pixTxid TEXT,
                    id_pedido INTEGER,
                    id_caixa INTEGER,
                    id_nota_fiscal INTEGER,
                    id_entrega INTEGER
                );

                CREATE TABLE IF NOT EXISTS cupons (
                    id_cupom INTEGER PRIMARY KEY AUTOINCREMENT,
                    chave_cupom TEXT,
                    valor_cupom REAL,
                    tipo_cupom TEXT,
                    id_pedido INTEGER
                );

                CREATE TABLE IF NOT EXISTS pedidos (
                    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
                    valor_total REAL,
                    observacoes TEXT,
                    id_pagamento INTEGER,
                    id_carrinho INTEGER,
                    id_cupom INTEGER,
                    id_servico INTEGER
                );

                CREATE TABLE IF NOT EXISTS rastreios (
                    id_rastreio INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo_rastreio INTEGER,
                    id_entrega INTEGER,
                    id_mensagem INTEGER
                );

                CREATE TABLE IF NOT EXISTS caixas (
                    id_caixa INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo_movimentacao TEXT,
                    valor REAL,
                    descricao TEXT,
                    data_movimentacao TEXT,
                    id_nota_fiscal INTEGER,
                    id_pagamento INTEGER
                );

                CREATE TABLE IF NOT EXISTS emails (
                    id_email INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT,
                    id_usuario INTEGER,
                    FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
                );

                CREATE TABLE IF NOT EXISTS carrinhos (
                    id_carrinho INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_servico INTEGER,
                    id_pedido INTEGER,
                    id_item_pedido INTEGER,
                    id_usuario INTEGER,
                    FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
                );

                CREATE TABLE IF NOT EXISTS servicos (
                    id_servico INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo_servico TEXT,
                    valor_servico REAL,
                    descricao TEXT,
                    id_pedido INTEGER,
                    id_orcamento INTEGER
                );

                CREATE TABLE IF NOT EXISTS mensagens (
                    id_mensagem INTEGER PRIMARY KEY AUTOINCREMENT,
                    mensagem TEXT,
                    tipo_mensagem TEXT,
                    id_pedido INTEGER,
                    id_email INTEGER,
                    id_orcamento INTEGER,
                    id_usuario INTEGER,
                    id_nota_fiscal INTEGER,
                    id_rastreio INTEGER,
                    FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
                );

                CREATE TABLE IF NOT EXISTS telefones (
                    id_telefone INTEGER PRIMARY KEY AUTOINCREMENT,
                    telefone_principal INTEGER,
                    telefone_secundario INTEGER,
                    id_usuario INTEGER,
                    FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
                );

                CREATE TABLE IF NOT EXISTS favoritos (
                    id_favoritos INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_produto INTEGER,
                    id_usuario INTEGER,
                    FOREIGN KEY(id_produto) REFERENCES produtos(id_produto),
                    FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
                );

                CREATE TABLE IF NOT EXISTS entregas (
                    id_entrega INTEGER PRIMARY KEY AUTOINCREMENT,
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
            """)
            # Ensure existing databases get the new column when migrating
            cursor.execute("PRAGMA table_info(usuarios)")
            columns = [row[1] for row in cursor.fetchall()]
            if "role" not in columns:
                cursor.execute("ALTER TABLE usuarios ADD COLUMN role TEXT DEFAULT 'user'")
        print("Banco de dados criado com sucesso!")