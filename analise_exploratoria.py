import pandas as pd
from sqlalchemy import create_engine

# Caminho do banco de dados
CAMINHO_BANCO = "test_analytics.db"
engine = create_engine(f"sqlite:///{CAMINHO_BANCO}")

def analise_exploratoria():
    """Realiza uma análise exploratória da quantidade de alunos por gênero em cada escola."""
    
    consulta_sql = """
        SELECT e.NOME AS nome_escola, 
               COUNT(CASE WHEN a.SEXO = 'M' THEN 1 END) AS qtd_masculino,
               COUNT(CASE WHEN a.SEXO = 'F' THEN 1 END) AS qtd_feminino
        FROM escolas_alunos ea
        JOIN escolas e ON ea.escola_id = e.ID
        JOIN alunos a ON ea.aluno_id = a.ID
        GROUP BY e.NOME;
    """
    
    # Executa a consulta e carrega os resultados em um DataFrame
    dados = pd.read_sql(consulta_sql, engine)

    if dados.empty:
        print("Nenhum dado encontrado. Verifique se as tabelas foram populadas corretamente.")
    else:
        print(dados)

if __name__ == "__main__":
    analise_exploratoria()
