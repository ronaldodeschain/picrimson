from app.database.crimson_database_pg import Database

def populate_all_tables():
    db = Database()
    
    try:
        with db.connect() as conn:
            cursor = conn.cursor()
            
            print("Iniciando povoamento das tabelas no PostgreSQL...")

            # 1. Usuários (Admin e Cliente de Teste)
            usuarios = [
                ('Admin Crimson', 'admin@crimson.com', 'admin123', '111.111.111-11', 'autenticado', 'admin'),
                ('Ronaldo Lemos', 'ronaldo@teste.com', 'cliente123', '222.222.222-22', 'nao_autenticado', 'user')
            ]
            cursor.executemany("""
                INSERT INTO usuarios (nome_usuario, login, senha, cpf, autenticado, role) 
                VALUES (%s, %s, %s, %s, %s, %s)
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

            # 3. Produtos
            produtos = [
                ('Estátua Crimson Claw', 'Estátua detalhada em resina', 250.0, 1),
                ('Chaveiro Garra', 'Chaveiro de metal personalizado', 25.0, 3)
            ]
            cursor.executemany("""
                INSERT INTO produtos (nome_produto, descricao, valor, id_categoria)
                VALUES (%s, %s, %s, %s)
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

            # 5. Avaliações (com destaque para exibir na home)
            avaliacoes = [
                ('A qualidade da impressão em resina superou minhas expectativas. Os detalhes da miniatura são incríveis!', 5.0, 1, 2, True),
                ('Pedi um projeto exclusivo e serviu perfeitamente. Atendimento nota 10.', 5.0, 2, 2, True),
                ('A pintura manual deu vida nova à minha estátua. Com certeza farei novos pedidos.', 4.0, 1, 2, True),
                ('Produto chegou bem embalado e dentro do prazo. Recomendo!', 4.0, 2, 2, False),
            ]
            cursor.executemany("""
                INSERT INTO avaliacoes (comentario, avaliacao, id_produto, id_usuario, destaque)
                VALUES (%s, %s, %s, %s, %s)
            """, avaliacoes)
            print("- Tabela 'avaliacoes' populada.")

            print("\nSucesso! O banco de dados PostgreSQL foi populado corretamente.")

    except Exception as e:
        print(f"Erro ao popular o banco de dados: {e}")

if __name__ == "__main__":
    # Certifique-se de que o DATABASE_TYPE está como 'postgres' no seu ambiente
    import os
    os.environ["DATABASE_TYPE"] = "postgres"
    populate_all_tables()