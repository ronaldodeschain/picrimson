from typing import cast, Union
from app.database.local import Database as SQLiteDatabase
from app.database.crimson_database_pg import Database as PostgresDatabase
from app.models.avaliacoes import Avaliacoes, AvaliacoesCriarAtualizar


class AvaliacoesRepository:
    def __init__(self, db: Union[SQLiteDatabase, PostgresDatabase]):
        self.db = db

    async def listar_avaliacoes(self) -> list[Avaliacoes]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM avaliacoes")
            linhas = cursor.fetchall()
            return [
                Avaliacoes(
                    id_avaliacao=linha[0],
                    comentario=linha[1],
                    avaliacao=linha[2],
                    id_produto=linha[3],
                    id_usuario=linha[4],
                    destaque=linha[5] if len(linha) > 5 else False
                ) for linha in linhas
            ]

    async def listar_avaliacoes_com_usuario(self) -> list[dict]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT a.comentario, a.avaliacao, u.nome_usuario "
                "FROM avaliacoes a "
                "LEFT JOIN usuarios u ON a.id_usuario = u.id_usuario"
            )
            linhas = cursor.fetchall()
            return [
                {
                    "comentario": linha[0],
                    "avaliacao": linha[1],
                    "nome_usuario": linha[2] if linha[2] else "Cliente satisfeito"
                }
                for linha in linhas
            ]

    async def listar_avaliacoes_destaque(self) -> list[dict]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT a.id_avaliacao, a.comentario, a.avaliacao, u.nome_usuario, p.nome_produto "
                "FROM avaliacoes a "
                "LEFT JOIN usuarios u ON a.id_usuario = u.id_usuario "
                "LEFT JOIN produtos p ON a.id_produto = p.id_produto "
                "WHERE a.destaque = TRUE "
                "ORDER BY a.avaliacao DESC"
            )
            linhas = cursor.fetchall()
            return [
                {
                    "id_avaliacao": linha[0],
                    "comentario": linha[1],
                    "avaliacao": linha[2],
                    "nome_usuario": linha[3] if linha[3] else "Cliente satisfeito",
                    "nome_produto": linha[4] if linha[4] else ""
                }
                for linha in linhas
            ]

    async def listar_avaliacoes_por_produto(self, id_produto: int) -> list[dict]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT a.id_avaliacao, a.comentario, a.avaliacao, u.nome_usuario, a.destaque "
                "FROM avaliacoes a "
                "LEFT JOIN usuarios u ON a.id_usuario = u.id_usuario "
                "WHERE a.id_produto = %s "
                "ORDER BY a.id_avaliacao DESC",
                (id_produto,)
            )
            linhas = cursor.fetchall()
            return [
                {
                    "id_avaliacao": linha[0],
                    "comentario": linha[1],
                    "avaliacao": linha[2],
                    "nome_usuario": linha[3] if linha[3] else "Cliente",
                    "destaque": linha[4]
                }
                for linha in linhas
            ]

    async def get_avaliacao_por_usuario_produto(self, id_usuario: int, id_produto: int) -> Avaliacoes | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT id_avaliacao, comentario, avaliacao, id_produto, id_usuario, destaque "
                "FROM avaliacoes WHERE id_usuario = %s AND id_produto = %s",
                (id_usuario, id_produto)
            )
            linha = cursor.fetchone()
            if linha:
                return Avaliacoes(
                    id_avaliacao=linha[0], comentario=linha[1], avaliacao=linha[2],
                    id_produto=linha[3], id_usuario=linha[4], destaque=linha[5] if len(linha) > 5 else False
                )
            return None

    async def listar_avaliacoes_com_usuario_produto(self) -> list[dict]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT a.id_avaliacao, a.comentario, a.avaliacao, a.destaque, "
                "u.nome_usuario, p.nome_produto, p.id_produto "
                "FROM avaliacoes a "
                "LEFT JOIN usuarios u ON a.id_usuario = u.id_usuario "
                "LEFT JOIN produtos p ON a.id_produto = p.id_produto "
                "ORDER BY a.id_avaliacao DESC"
            )
            linhas = cursor.fetchall()
            return [
                {
                    "id_avaliacao": linha[0],
                    "comentario": linha[1],
                    "avaliacao": linha[2],
                    "destaque": linha[3],
                    "nome_usuario": linha[4] if linha[4] else "Cliente",
                    "nome_produto": linha[5] if linha[5] else "Produto removido",
                    "id_produto": linha[6]
                }
                for linha in linhas
            ]

    async def toggle_destaque(self, avaliacao_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE avaliacoes SET destaque = NOT destaque WHERE id_avaliacao = %s",
                (avaliacao_id,)
            )
            return cursor.rowcount > 0

    async def get_avaliacao(self, avaliacao_id: int) -> Avaliacoes | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT id_avaliacao, comentario, avaliacao, id_produto, id_usuario, destaque FROM avaliacoes WHERE id_avaliacao = %s",
                (avaliacao_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Avaliacoes(
                    id_avaliacao=linha[0],
                    comentario=linha[1],
                    avaliacao=linha[2],
                    id_produto=linha[3],
                    id_usuario=linha[4],
                    destaque=linha[5] if len(linha) > 5 else False
                )
            return None

    async def criar_avaliacao(self,
                avaliacao: AvaliacoesCriarAtualizar) -> Avaliacoes | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO avaliacoes(comentario, avaliacao, id_produto, id_usuario, destaque) VALUES (%s, %s, %s, %s, %s) RETURNING id_avaliacao",
                (avaliacao.comentario, avaliacao.avaliacao, avaliacao.id_produto, avaliacao.id_usuario, avaliacao.destaque)
            )
            id_avaliacao = cursor.fetchone()[0] #type:ignore
            return Avaliacoes(
                id_avaliacao=id_avaliacao,
                comentario=avaliacao.comentario,
                avaliacao=avaliacao.avaliacao,
                id_produto=avaliacao.id_produto,
                id_usuario=avaliacao.id_usuario,
                destaque=avaliacao.destaque
            )

    async def update_avaliacao(self, avaliacao_id: int,
                    avaliacao: AvaliacoesCriarAtualizar) -> Avaliacoes | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE avaliacoes SET comentario = %s, avaliacao = %s, id_produto = %s, id_usuario = %s, destaque = %s WHERE id_avaliacao = %s",
                (avaliacao.comentario, avaliacao.avaliacao, avaliacao.id_produto, avaliacao.id_usuario, avaliacao.destaque, avaliacao_id)
            )
            if cursor.rowcount == 0:
                return None
            return Avaliacoes(
                id_avaliacao=avaliacao_id,
                comentario=avaliacao.comentario,
                avaliacao=avaliacao.avaliacao,
                id_produto=avaliacao.id_produto,
                id_usuario=avaliacao.id_usuario,
                destaque=avaliacao.destaque
            )

    async def delete_avaliacao(self, avaliacao_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "DELETE FROM avaliacoes WHERE id_avaliacao = %s",
                (avaliacao_id,)
            )
            return cursor.rowcount > 0