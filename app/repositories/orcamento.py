from typing import cast
from app.database.local import Database
from app.models.orcamento import Orcamento, OrcamentoCriarAtualizar


class OrcamentoRepository:
    def __init__(self, db: Database):
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
                ) for linha in linhas
            ]

    async def get_orcamento(self, orcamento_id: int) -> Orcamento | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM orcamentos WHERE id_orcamento = ?",
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
                )
            return None

    async def criar_orcamento(self, orcamento: OrcamentoCriarAtualizar) -> Orcamento:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO orcamentos (mensagem, arquivo, imagem, id_mensagem, id_servico) VALUES (?, ?, ?, ?, ?)",
                (orcamento.mensagem, orcamento.arquivo, orcamento.imagem, orcamento.id_mensagem, orcamento.id_servico)
            )
            id_orcamento = cast(int, cursor.lastrowid)
            return Orcamento(
                id_orcamento=id_orcamento,
                mensagem=orcamento.mensagem,
                arquivo=orcamento.arquivo,
                imagem=orcamento.imagem,
                id_mensagem=orcamento.id_mensagem,
                id_servico=orcamento.id_servico
            )  # type: ignore

    async def update_orcamento(self, orcamento_id: int, orcamento: OrcamentoCriarAtualizar) -> Orcamento | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE orcamentos SET mensagem = ?, arquivo = ?, imagem = ?, id_mensagem = ?, id_servico = ? WHERE id_orcamento = ?",
                (orcamento.mensagem, orcamento.arquivo, orcamento.imagem, orcamento.id_mensagem, orcamento.id_servico, orcamento_id)
            )
            if cursor.rowcount > 0:
                return Orcamento(
                    id_orcamento=orcamento_id,
                    mensagem=orcamento.mensagem,
                    arquivo=orcamento.arquivo,
                    imagem=orcamento.imagem,
                    id_mensagem=orcamento.id_mensagem,
                    id_servico=orcamento.id_servico
                )
            return None

    async def delete_orcamento(self, orcamento_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("DELETE FROM orcamentos WHERE id_orcamento = ?", (orcamento_id,))
            return cursor.rowcount > 0