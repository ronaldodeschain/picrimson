from typing import cast
from app.database.local import Database
from app.models.endereco import Endereco, EnderecoCriarAtualizar


class EnderecoRepository:
    def __init__(self, db: Database):
        self.db = db

    async def listar_enderecos(self) -> list[Endereco]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM enderecos")
            linhas = cursor.fetchall()
            return [
                Endereco(
                    id_endereco=linha[0],
                    rua=linha[1],
                    numero=linha[2],
                    complemento=linha[3],
                    cep=linha[4],
                    cidade=linha[5],
                    estado=linha[6],
                    observacoes=linha[7],
                    id_usuario=linha[8]
                ) for linha in linhas
            ]

    async def get_endereco(self, endereco_id: int) -> Endereco | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM enderecos WHERE id_endereco = ?",
                (endereco_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Endereco(
                    id_endereco=linha[0],
                    rua=linha[1],
                    numero=linha[2],
                    complemento=linha[3],
                    cep=linha[4],
                    cidade=linha[5],
                    estado=linha[6],
                    observacoes=linha[7],
                    id_usuario=linha[8]
                )
            return None

    async def criar_endereco(self,
                              endereco: EnderecoCriarAtualizar) -> Endereco | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO enderecos(rua, numero, complemento, cep, cidade, estado, observacoes, id_usuario) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (endereco.rua, endereco.numero, endereco.complemento, endereco.cep, endereco.cidade, endereco.estado, endereco.observacoes, endereco.id_usuario)
            )
            id_endereco = cast(int, cursor.lastrowid)
            return Endereco(
                id_endereco=id_endereco,
                rua=endereco.rua,
                numero=endereco.numero,
                complemento=endereco.complemento,
                cep=endereco.cep,
                cidade=endereco.cidade,
                estado=endereco.estado,
                observacoes=endereco.observacoes,
                id_usuario=endereco.id_usuario
            )

    async def update_endereco(self, endereco_id: int,
                              endereco: EnderecoCriarAtualizar) -> Endereco | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE enderecos SET rua = ?, numero = ?, complemento = ?, cep = ?, cidade = ?, estado = ?, observacoes = ?, id_usuario = ? WHERE id_endereco = ?",
                (endereco.rua, endereco.numero, endereco.complemento, endereco.cep, endereco.cidade, endereco.estado, endereco.observacoes, endereco.id_usuario, endereco_id)
            )
            if cursor.rowcount == 0:
                return None
            return Endereco(
                id_endereco=endereco_id,
                rua=endereco.rua,
                numero=endereco.numero,
                complemento=endereco.complemento,
                cep=endereco.cep,
                cidade=endereco.cidade,
                estado=endereco.estado,
                observacoes=endereco.observacoes,
                id_usuario=endereco.id_usuario
            )

    async def delete_endereco(self, endereco_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "DELETE FROM enderecos WHERE id_endereco = ?",
                (endereco_id,)
            )
            return cursor.rowcount > 0