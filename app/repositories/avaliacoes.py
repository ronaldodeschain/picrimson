from typing import cast
from app.database.local import Database
from app.models.avaliacoes import Avaliacoes, AvaliacoesCriarAtualizar


class AvaliacoesRepository:
    def __init__(self, db: Database):
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
                    id_usuario=linha[4]
                ) for linha in linhas
            ]

    async def get_avaliacao(self, avaliacao_id: int) -> Avaliacoes | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM avaliacoes WHERE id_avaliacao = ?",
                (avaliacao_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Avaliacoes(
                    id_avaliacao=linha[0],
                    comentario=linha[1],
                    avaliacao=linha[2],
                    id_produto=linha[3],
                    id_usuario=linha[4]
                )
            return None

    async def criar_avaliacao(self,
                               avaliacao: AvaliacoesCriarAtualizar) -> Avaliacoes | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO avaliacoes(comentario, avaliacao, id_produto, id_usuario) VALUES (?, ?, ?, ?)",
                (avaliacao.comentario, avaliacao.avaliacao, avaliacao.id_produto, avaliacao.id_usuario)
            )
            id_avaliacao = cast(int, cursor.lastrowid)
            return Avaliacoes(
                id_avaliacao=id_avaliacao,
                comentario=avaliacao.comentario,
                avaliacao=avaliacao.avaliacao,
                id_produto=avaliacao.id_produto,
                id_usuario=avaliacao.id_usuario
            )

    async def update_avaliacao(self, avaliacao_id: int,
                               avaliacao: AvaliacoesCriarAtualizar) -> Avaliacoes | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE avaliacoes SET comentario = ?, avaliacao = ?, id_produto = ?, id_usuario = ? WHERE id_avaliacao = ?",
                (avaliacao.comentario, avaliacao.avaliacao, avaliacao.id_produto, avaliacao.id_usuario, avaliacao_id)
            )
            if cursor.rowcount == 0:
                return None
            return Avaliacoes(
                id_avaliacao=avaliacao_id,
                comentario=avaliacao.comentario,
                avaliacao=avaliacao.avaliacao,
                id_produto=avaliacao.id_produto,
                id_usuario=avaliacao.id_usuario
            )

    async def delete_avaliacao(self, avaliacao_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "DELETE FROM avaliacoes WHERE id_avaliacao = ?",
                (avaliacao_id,)
            )
            return cursor.rowcount > 0