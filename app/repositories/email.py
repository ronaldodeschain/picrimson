import sqlite3
from typing import List, Optional, cast
from app.models.email import Email, EmailCriarAtualizar
from app.database.local import Database


class EmailRepository:
    def __init__(self, db: Database):
        self.db = db

    async def listar_emails(self) -> List[Email]:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_email, email, id_usuario FROM emails")
            rows = cursor.fetchall()
            return [Email(id_email=row[0], email=row[1], id_usuario=row[2]) for row in rows]

    async def get_email(self, id_email: int) -> Optional[Email]:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_email, email, id_usuario FROM emails WHERE id_email = ?", (id_email,))
            row = cursor.fetchone()
            if row:
                return Email(id_email=row[0], email=row[1], id_usuario=row[2])
            return None

    async def criar_email(self, email: EmailCriarAtualizar) -> Email:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO emails (email, id_usuario) VALUES (?, ?)",
                (email.email, email.id_usuario)
            )
            id_email = cast(int, cursor.lastrowid)
            return Email(id_email=id_email, email=email.email, id_usuario=email.id_usuario)  # type: ignore

    async def update_email(self, id_email: int, email: EmailCriarAtualizar) -> Optional[Email]:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE emails SET email = ?, id_usuario = ? WHERE id_email = ?",
                (email.email, email.id_usuario, id_email)
            )
            if cursor.rowcount > 0:
                return Email(id_email=id_email, email=email.email, id_usuario=email.id_usuario)
            return None

    async def delete_email(self, id_email: int) -> bool:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM emails WHERE id_email = ?", (id_email,))
            deleted = cursor.rowcount > 0
            return deleted