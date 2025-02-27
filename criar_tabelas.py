import sqlite3


DB_PATH = "test_analytics.db"


def criar_tabelas():

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Criar tabela escolas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS escolas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                CODESC TEXT UNIQUE,
                NOME TEXT
            );
        """)

        # Criar tabela alunos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                CODESC TEXT,
                SEXO TEXT
            );
        """)

        # Criar tabela de relacionamento escolas_alunos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS escolas_alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                escola_id INTEGER,
                aluno_id INTEGER,
                FOREIGN KEY (escola_id) REFERENCES escolas(id),
                FOREIGN KEY (aluno_id) REFERENCES alunos(id)
            );
        """)

        # Commit para garantir que as alterações sejam salvas
        conn.commit()

    print("Tabelas criadas com sucesso!")

# Chamar a função para criar as tabelas
if __name__ == "__main__":
    criar_tabelas()
