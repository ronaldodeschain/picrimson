import os
import random
import string
import unittest
from fastapi.testclient import TestClient

# Ensure Postgres is used for the test run
os.environ.setdefault("DATABASE_TYPE", "postgres")
os.environ.setdefault("DB_NAME", "crimson_db")
os.environ.setdefault("DB_USER", "postgres")
os.environ.setdefault("DB_PASS", "postgres")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")

from app.main import app
from app.database.crimson_database_pg import Database as PostgresDatabase


def generate_valid_cpf() -> str:
    """Generate a valid CPF using the standard Brazil CPF check digit algorithm."""
    digits = [random.randint(0, 9) for _ in range(9)]

    def calc_digit(nums):
        weight = len(nums) + 1
        total = sum(d * w for d, w in zip(nums, range(weight, 1, -1)))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    first = calc_digit(digits)
    second = calc_digit(digits + [first])
    return "".join(str(d) for d in digits + [first, second])


def random_email() -> str:
    suffix = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    return f"test_{suffix}@example.com"


class AuthTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.database = PostgresDatabase()

    def setUp(self):
        self.created_emails = []

    def tearDown(self):
        self._cleanup_test_users()

    def _cleanup_test_users(self):
        if not self.created_emails:
            return

        with self.database.connect() as connection:
            cursor = connection.cursor()
            for email in self.created_emails:
                cursor.execute("DELETE FROM email WHERE email = %s", (email,))
                cursor.execute("DELETE FROM usuarios WHERE login = %s", (email,))

    def _register_user(self, nome, email, senha, cpf):
        response = self.client.post(
            "/cadastro",
            data={
                "nome": nome,
                "email": email,
                "senha": senha,
                "cpf": cpf,
            },
        )
        if response.status_code == 200 and "Cadastro realizado com sucesso" in response.text:
            self.created_emails.append(email)
        return response

    def test_01_cadastro_com_dados_validos(self):
        email = random_email()
        cpf = generate_valid_cpf()

        response = self._register_user(
            nome="Usuario de Teste",
            email=email,
            senha="SenhaForte123",
            cpf=cpf,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Cadastro realizado com sucesso", response.text)

        login_response = self.client.post(
            "/login.html",
            data={"email": email, "password": "SenhaForte123"},
        )
        self.assertTrue(any(resp.status_code == 303 for resp in login_response.history), "Expected login redirect")
        self.assertTrue(str(login_response.url).endswith("/minha-conta"))

    def test_02_cadastro_com_email_ja_existente(self):
        email = random_email()
        cpf = generate_valid_cpf()

        first_response = self._register_user(
            nome="Usuario Inicial",
            email=email,
            senha="SenhaForte123",
            cpf=cpf,
        )
        self.assertEqual(first_response.status_code, 200)
        self.assertIn("Cadastro realizado com sucesso", first_response.text)

        duplicate_response = self._register_user(
            nome="Outro Usuario",
            email=email,
            senha="OutraSenha456",
            cpf=generate_valid_cpf(),
        )
        self.assertEqual(duplicate_response.status_code, 200)
        self.assertIn("Este e-mail já está cadastrado no sistema", duplicate_response.text)

    def test_03_cadastro_campos_obrigatorios_vazios(self):
        response = self.client.post(
            "/cadastro",
            data={"nome": " ", "email": " ", "senha": " ", "cpf": " "},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Todos os campos obrigatórios devem ser preenchidos", response.text)

    def test_04_login_validacao_de_acesso(self):
        email = random_email()
        cpf = generate_valid_cpf()

        response = self._register_user(
            nome="Usuario Login",
            email=email,
            senha="SenhaLogin123",
            cpf=cpf,
        )
        self.assertEqual(response.status_code, 200)

        login_response = self.client.post(
            "/login.html",
            data={"email": email, "password": "SenhaLogin123"},
        )
        self.assertTrue(any(resp.status_code == 303 for resp in login_response.history), "Expected login redirect")
        self.assertTrue(str(login_response.url).endswith("/minha-conta"))

    def test_05_login_com_senha_incorreta(self):
        email = random_email()
        cpf = generate_valid_cpf()

        response = self._register_user(
            nome="Usuario Senha Errada",
            email=email,
            senha="SenhaCorreta123",
            cpf=cpf,
        )
        self.assertEqual(response.status_code, 200)

        login_response = self.client.post(
            "/login.html",
            data={"email": email, "password": "SenhaErrada456"},
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertIn("Email ou senha inválidos", login_response.text)

    def test_06_login_com_usuario_inexistente(self):
        login_response = self.client.post(
            "/login.html",
            data={"email": random_email(), "password": "SenhaQualquer123"},
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertIn("Email ou senha inválidos", login_response.text)


if __name__ == "__main__":
    unittest.main()
