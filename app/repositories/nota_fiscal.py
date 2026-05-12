from datetime import date
from typing import cast, Union
from app.database.local import Database as SQLiteDatabase
from app.database.crimson_database_pg import Database as PostgresDatabase
from app.models.nota_fiscal import NotaFiscal, NotaFiscalCriarAtualizar


class NotaFiscalRepository:
    def __init__(self, db: Union[SQLiteDatabase, PostgresDatabase]):
        self.db = db

    async def listar_notas_fiscais(self) -> list[NotaFiscal]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM notas_fiscais")
            linhas = cursor.fetchall()
            return [
                NotaFiscal(
                    id_nota_fiscal=linha[0],
                    forma_pagamento=linha[1],
                    data_emissao=date.fromisoformat(linha[2]),
                    serie=linha[3],
                    numero=linha[4],
                    status=linha[5],
                    id_caixa=linha[7],
                    id_pagamento=linha[8],
                    id_mensagem=linha[9]
                ) for linha in linhas
            ]

    async def get_nota_fiscal(self, nota_id: int) -> NotaFiscal | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM notas_fiscais WHERE id_nota_fiscal = %s",
                (nota_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return NotaFiscal(
                    id_nota_fiscal=linha[0],
                    forma_pagamento=linha[1],
                    data_emissao=date.fromisoformat(linha[2]),
                    serie=linha[3],
                    numero=linha[4],
                    status=linha[5],
                    id_caixa=linha[7],
                    id_pagamento=linha[8],
                    id_mensagem=linha[9]
                )
            return None

    async def criar_nota_fiscal(self, nota: NotaFiscalCriarAtualizar) -> NotaFiscal:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO notas_fiscais (forma_pagamento, data_emissao, serie, numero, status, id_caixa, id_pagamento, id_mensagem) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_nota_fiscal",
                (nota.forma_pagamento, nota.data_emissao.isoformat(), nota.serie, nota.numero, nota.status, nota.id_caixa, nota.id_pagamento, nota.id_mensagem)
            )
            id_nota_fiscal = cursor.fetchone()[0]
            return NotaFiscal(
                id_nota_fiscal=id_nota_fiscal,
                forma_pagamento=nota.forma_pagamento,
                data_emissao=nota.data_emissao,
                serie=nota.serie,
                numero=nota.numero,
                status=nota.status,
                id_caixa=nota.id_caixa,
                id_pagamento=nota.id_pagamento,
                id_mensagem=nota.id_mensagem
            )  # type: ignore

    async def update_nota_fiscal(self, nota_id: int, nota: NotaFiscalCriarAtualizar) -> NotaFiscal | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE notas_fiscais SET forma_pagamento = %s, data_emissao = %s, serie = %s, numero = %s, status = %s, id_caixa = %s, id_pagamento = %s, id_mensagem = %s WHERE id_nota_fiscal = %s",
                (nota.forma_pagamento, nota.data_emissao.isoformat(), nota.serie, nota.numero, nota.status, nota.id_caixa, nota.id_pagamento, nota.id_mensagem, nota_id)
            )
            if cursor.rowcount > 0:
                return NotaFiscal(
                    id_nota_fiscal=nota_id,
                    forma_pagamento=nota.forma_pagamento,
                    data_emissao=nota.data_emissao,
                    serie=nota.serie,
                    numero=nota.numero,
                    status=nota.status,
                    id_caixa=nota.id_caixa,
                    id_pagamento=nota.id_pagamento,
                    id_mensagem=nota.id_mensagem
                )
            return None

    async def delete_nota_fiscal(self, nota_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("DELETE FROM notas_fiscais WHERE id_nota_fiscal = %s", (nota_id,))
            return cursor.rowcount > 0