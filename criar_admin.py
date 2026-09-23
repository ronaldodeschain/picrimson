"""
Cria um usuário admin no banco de dados.
Uso: python criar_admin.py
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Dados do admin
NOME = "Admin"
EMAIL = "admin@crimsonclaw.com"
SENHA = "admin1234"
CPF = "00000000000"

def criar_admin_sqlite():
    from app.database.local import Database
    db = Database()
    with db.connect() as conn:
        cursor = conn.cursor()

        # Verifica se já existe
        cursor.execute("SELECT id_usuario FROM usuarios WHERE login = %s", (EMAIL,))
        if cursor.fetchone():
            print(f"Usuário '{EMAIL}' já existe.")
            return

        cursor.execute(
            "INSERT INTO usuarios(nome_usuario, login, senha, cpf, autenticado, role) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_usuario",
            (NOME, EMAIL, SENHA, CPF, "autenticado", "admin")
        )
        id_usuario = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO email(email, id_usuario) VALUES (%s, %s)",
            (EMAIL, id_usuario)
        )
    print(f"Admin criado com sucesso!")
    print(f"  Email: {EMAIL}")
    print(f"  Senha: {SENHA}")


def criar_admin_postgres():
    from app.database.crimson_database_pg import Database
    db = Database()
    with db.connect() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT id_usuario FROM usuarios WHERE login = %s", (EMAIL,))
        if cursor.fetchone():
            print(f"Usuário '{EMAIL}' já existe.")
            return

        cursor.execute(
            "INSERT INTO usuarios(nome_usuario, login, senha, cpf, autenticado, role) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_usuario",
            (NOME, EMAIL, SENHA, CPF, "autenticado", "admin")
        )
        id_usuario = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO email(email, id_usuario) VALUES (%s, %s)",
            (EMAIL, id_usuario)
        )
    print(f"Admin criado com sucesso!")
    print(f"  Email: {EMAIL}")
    print(f"  Senha: {SENHA}")


if __name__ == "__main__":
    db_type = os.getenv("DATABASE_TYPE", "sqlite")
    if db_type == "postgres":
        criar_admin_postgres()
    else:
        criar_admin_sqlite()
