from typing import cast, Union
from app.database.local import Database as SQLiteDatabase
from app.database.crimson_database_pg import Database as PostgresDatabase
from app.models.orcamento import Orcamento, OrcamentoCriarAtualizar


class OrcamentoRepository:
    def __init__(self, db: Union[SQLiteDatabase, PostgresDatabase]):
        self.db = db

    async def listar_orcamentos(self) -> list[Orcamento]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM orcamentos")
            linhas = cursor.fetchall()
            return [
                Orcamento(
                    id_orcamento=linha[0],
                    mensagem=linha[1],
                    arquivo=linha[2],
                    imagem=linha[3],
                    id_mensagem=linha[4],
                    id_servico=linha[5]
                    , nome=linha[6] if len(linha) > 6 else None
                    , contato=linha[7] if len(linha) > 7 else None
                    , tipo_projeto=linha[8] if len(linha) > 8 else None
                    , descricao=linha[9] if len(linha) > 9 else None
                    , tamanho_desejado=linha[10] if len(linha) > 10 else None
                ) for linha in linhas
            ]

    async def get_orcamento(self, orcamento_id: int) -> Orcamento | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM orcamentos WHERE id_orcamento = %s",
                (orcamento_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Orcamento(
                    id_orcamento=linha[0],
                    mensagem=linha[1],
                    arquivo=linha[2],
                    imagem=linha[3],
                    id_mensagem=linha[4],
                    id_servico=linha[5]
                    , nome=linha[6] if len(linha) > 6 else None
                    , contato=linha[7] if len(linha) > 7 else None
                    , tipo_projeto=linha[8] if len(linha) > 8 else None
                    , descricao=linha[9] if len(linha) > 9 else None
                    , tamanho_desejado=linha[10] if len(linha) > 10 else None
                )
            return None

    async def criar_orcamento(self, orcamento: OrcamentoCriarAtualizar) -> Orcamento:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO orcamentos (mensagem, arquivo, imagem, id_mensagem, id_servico, nome, contato, tipo_projeto, descricao, tamanho_desejado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_orcamento",
                (orcamento.mensagem, orcamento.arquivo, orcamento.imagem, orcamento.id_mensagem, orcamento.id_servico, orcamento.nome, orcamento.contato, orcamento.tipo_projeto, orcamento.descricao, orcamento.tamanho_desejado)
            )
            id_orcamento = cursor.fetchone()[0]
            return Orcamento(
                id_orcamento=id_orcamento,
                mensagem=orcamento.mensagem,
                arquivo=orcamento.arquivo,
                imagem=orcamento.imagem,
                id_mensagem=orcamento.id_mensagem,
                id_servico=orcamento.id_servico
                    , nome=orcamento.nome
                    , contato=orcamento.contato
                    , tipo_projeto=orcamento.tipo_projeto
                    , descricao=orcamento.descricao
                    , tamanho_desejado=orcamento.tamanho_desejado
            )  # type: ignore

    async def update_orcamento(self, orcamento_id: int, orcamento: OrcamentoCriarAtualizar) -> Orcamento | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE orcamentos SET mensagem = %s, arquivo = %s, imagem = %s, id_mensagem = %s, id_servico = %s, nome = %s, contato = %s, tipo_projeto = %s, descricao = %s, tamanho_desejado = %s WHERE id_orcamento = %s",
                (orcamento.mensagem, orcamento.arquivo, orcamento.imagem, orcamento.id_mensagem, orcamento.id_servico, orcamento.nome, orcamento.contato, orcamento.tipo_projeto, orcamento.descricao, orcamento.tamanho_desejado, orcamento_id)
            )
            if cursor.rowcount > 0:
                return Orcamento(
                    id_orcamento=orcamento_id,
                    mensagem=orcamento.mensagem,
                    arquivo=orcamento.arquivo,
                    imagem=orcamento.imagem,
                    id_mensagem=orcamento.id_mensagem,
                    id_servico=orcamento.id_servico
                    , nome=orcamento.nome
                    , contato=orcamento.contato
                    , tipo_projeto=orcamento.tipo_projeto
                    , descricao=orcamento.descricao
                    , tamanho_desejado=orcamento.tamanho_desejado
                )
            return None

    async def delete_orcamento(self, orcamento_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("DELETE FROM orcamentos WHERE id_orcamento = %s", (orcamento_id,))
            return cursor.rowcount > 0