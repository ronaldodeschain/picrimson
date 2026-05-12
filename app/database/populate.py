from app.database.crimson_database_pg import Database

def populate_all_tables():
    db = Database()
    
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            
            print("Iniciando povoamento das tabelas no PostgreSQL...")

            # 1. Usuários (Admin e Cliente de Teste)
            usuarios = [
                ('Admin Crimson', 'admin@crimson.com', 'admin123', '111.111.111-11', 'admin'),
                ('Ronaldo Lemos', 'ronaldo@teste.com', 'cliente123', '222.222.222-22', 'user')
            ]
            cursor.executemany("""
                INSERT INTO usuarios (nome_usuario, login, senha, cpf, role) 
                VALUES (%s, %s, %s, %s, %s)
            """, usuarios)
            print("- Tabela 'usuarios' populada.")

            # 2. Categorias
            categorias = [
                ('Action Figures',),
                ('Colecionáveis',),
                ('Acessórios',)
            ]
            cursor.executemany("INSERT INTO categorias (nome_categoria) VALUES (%s)", categorias)
            print("- Tabela 'categorias' populada.")

            # 3. Produtos (Exemplo vinculado à categoria 1)
            produtos = [
                ('Estátua Crimson Claw', 'Estátua detalhada em resina', 'Resina', 30.0, 15.0, 15.0, 10, 1.5, 250.0, 1),
                ('Chaveiro Garra', 'Chaveiro de metal personalizado', 'Metal', 5.0, 2.0, 0.5, 50, 0.05, 25.0, 3)
            ]
            cursor.executemany("""
                INSERT INTO produtos (
                    nome_produto, descricao, material, altura, comprimento, largura, 
                    quantidade, peso, valor, id_categoria
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, produtos)
            print("- Tabela 'produtos' populada.")

            # 4. Endereços
            enderecos = [
                ('Rua das Flores', 123, 'Apto 1', '01234-567', 'São Paulo', 'SP', 'Perto do metrô', 2)
            ]
            cursor.executemany("""
                INSERT INTO enderecos (rua, numero, complemento, cep, cidade, estado, observacoes, id_usuario)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, enderecos)
            print("- Tabela 'enderecos' populada.")

            print("\nSucesso! O banco de dados PostgreSQL foi populado corretamente.")

    except Exception as e:
        print(f"Erro ao popular o banco de dados: {e}")

if __name__ == "__main__":
    # Certifique-se de que o DATABASE_TYPE está como 'postgres' no seu ambiente
    import os
    os.environ["DATABASE_TYPE"] = "postgres"
    populate_all_tables()