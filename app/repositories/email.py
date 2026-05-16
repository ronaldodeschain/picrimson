from typing import List, Optional, cast, Union
from app.models.email import Email, EmailCriarAtualizar
from app.database.local import Database as SQLiteDatabase
from app.database.crimson_database_pg import Database as PostgresDatabase

class EmailRepository:
    def __init__(self, db: Union[SQLiteDatabase, PostgresDatabase]):
        self.db = db

    async def listar_emails(self) -> List[Email]:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_email, email, id_usuario FROM email")
            rows = cursor.fetchall()
            return [Email(id_email=row[0], email=row[1], id_usuario=row[2]) for row in rows]

    async def get_email(self, id_email: int) -> Optional[Email]:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_email, email, id_usuario FROM email WHERE id_email = %s", (id_email,))
            row = cursor.fetchone()
            if row:
                return Email(id_email=row[0], email=row[1], id_usuario=row[2])
            return None

    async def get_email_por_valor(self, email_val: str) -> Optional[Email]:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_email, email, id_usuario FROM email WHERE email = %s", (email_val,))
            row = cursor.fetchone()
            if row:
                return Email(id_email=row[0], email=row[1], id_usuario=row[2])
            return None

    async def criar_email(self, email: EmailCriarAtualizar) -> Email:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO email (email, id_usuario) VALUES (%s, %s) RETURNING id_email",
                (email.email, email.id_usuario)
            )
            id_email = cursor.fetchone()[0]
            return Email(id_email=id_email, email=email.email, id_usuario=email.id_usuario)  # type: ignore

    async def update_email(self, id_email: int, email: EmailCriarAtualizar) -> Optional[Email]:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE email SET email = %s, id_usuario = %s WHERE id_email = %s",
                (email.email, email.id_usuario, id_email)
            )
            if cursor.rowcount > 0:
                return Email(id_email=id_email, email=email.email, id_usuario=email.id_usuario)
            return None

    async def delete_email(self, id_email: int) -> bool:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM email WHERE id_email = %s", (id_email,))
            deleted = cursor.rowcount > 0
            return deleted