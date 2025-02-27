from sqlalchemy import create_engine, text
import pandas as pd
import glob
import os

# Caminho do banco de dados
CAMINHO_DB = "test_analytics.db"
engine = create_engine(f"sqlite:///{CAMINHO_DB}")

# Diretórios dos arquivos CSV
PASTA_ESCOLAS = "data/escolas"  # Pasta das escolas
PASTA_ALUNOS = "data/perfil dos educandos"  # Pasta dos alunos

# Lista de arquivos de escolas
arquivos_escolas = [
    "data/escolas/._escolas122018.csv", "data/escolas/._escolas122019.csv", 
    "data/escolas/._escolas122020.csv", "data/escolas/._escolas122021.csv", 
    "data/escolas/._escolas122022.csv", "data/escolas/._escolas122023.csv", 
    "data/escolas/._escolas-dez-2010.csv", "data/escolas/._escolas-dez-2011.csv", 
    "data/escolas/._escolas-dez-2012.csv", "data/escolas/._escolas-dez-2013.csv", 
    "data/escolas/._escolas-dez-2014.csv", "data/escolas/._escolas-dez-2015.csv", 
    "data/escolas/._escolasr34.csv", "data/escolas/._escolasr34dez2017.csv"
]

# Lista de arquivos de perfil dos educandos
arquivos_alunos = [
    "data/perfil dos educandos/idadeserieneeracadez17.csv", 
    "data/perfil dos educandos/idadeserieneeracadez18.csv", 
    "data/perfil dos educandos/idadeserieneeracadez19.csv", 
    "data/perfil dos educandos/idadeserieneeracadez20.csv", 
    "data/perfil dos educandos/idadeserieneeracadez21.csv", 
    "data/perfil dos educandos/idadeserieneeracadez22.csv", 
    "data/perfil dos educandos/idadeserieneeracadez23.csv", 
    "data/perfil dos educandos/idadeserieneeraca-r33.csv"
]

# Esquema esperado para a tabela de escolas (nomes das colunas)
ESCOLAS_SCHEMA = [
    'ID', 'NOME', 'CODESC', 'CNPJ', 'MUNICIPIO', 'UF', 'LATITUDE', 'LONGITUDE', 'CEP', 'TIPO',
    'DEPENDENCIA', 'LOCALIZACAO', 'REGIAO', 'TURNO', 'DATA'
]

# Esquema esperado para a tabela de alunos (nomes das colunas)
ALUNOS_SCHEMA = [
    'ID', 'CODESC', 'NOME', 'IDADE', 'ANO', 'SITUACAO', 'ESCOLARIDADE', 'SEXO', 'ETNIA', 'MUNICIPIO', 'UF', 'REGIAO', 'DATA'
]

# Correções dos nomes das colunas (se necessário)
ESCOLAS_CORRECOES = {
    'CÓDIGO': 'CODESC',
    'NOME DA ESCOLA': 'NOME',
    'LATITUDE': 'LATITUDE',
    'LONGITUDE': 'LONGITUDE',
    'CEP': 'CEP',
    'CNPJ': 'CNPJ',
    'MUNICÍPIO': 'MUNICIPIO',
    'UF': 'UF',
    'TIPO': 'TIPO',
    'DEPENDÊNCIA': 'DEPENDENCIA',
    'LOCALIZAÇÃO': 'LOCALIZACAO',
    'REGIÃO': 'REGIAO',
    'TURNO': 'TURNO',
    'DATA': 'DATA'
}

ALUNOS_CORRECOES = {
    'CODESC': 'CODESC',
    'NOME': 'NOME',
    'IDADE': 'IDADE',
    'ANO': 'ANO',
    'SITUAÇÃO': 'SITUACAO',
    'ESCOLARIDADE': 'ESCOLARIDADE',
    'SEXO': 'SEXO',
    'ETNIA': 'ETNIA',
    'MUNICÍPIO': 'MUNICIPIO',
    'UF': 'UF',
    'REGIÃO': 'REGIAO',
    'DATA': 'DATA'
}

# Função para normalizar os cabeçalhos dos arquivos CSV
def normalizar_cabecalho(df, schema, correcoes):
    """Aplica correções no cabeçalho do arquivo CSV."""
    df.columns = [correcoes.get(col.strip().upper(), col.strip().upper()) for col in df.columns]
    # Adiciona colunas faltantes
    for col in schema:
        if col not in df.columns:
            df[col] = pd.NA
    # Remove colunas extras
    for col in df.columns:
        if col not in schema:
            df = df.drop(columns=[col])
    # Remove colunas duplicadas
    df = df.drop(df.columns[df.columns.duplicated()], axis=1)
    return df

# Função para carregar os dados das pastas de Escolas e Alunos
def carregar_dados():
    """Realiza o carregamento dos arquivos .csv das pastas Escolas e Perfil dos educandos."""
    # Carregar dados das Escolas
    for arquivo in arquivos_escolas:
        print(f"Carregando arquivo: {arquivo}")
        df = pd.read_csv(arquivo, sep=';', encoding='latin1')
        df = normalizar_cabecalho(df, ESCOLAS_SCHEMA, ESCOLAS_CORRECOES)
        df.to_sql("escolas", con=engine, if_exists="append", index=False)
    
    # Carregar dados dos Alunos
    for arquivo in arquivos_alunos:
        print(f"Carregando arquivo: {arquivo}")
        df = pd.read_csv(arquivo, sep=';', encoding='latin1')
        df = normalizar_cabecalho(df, ALUNOS_SCHEMA, ALUNOS_CORRECOES)
        df.to_sql("alunos", con=engine, if_exists="append", index=False)
    print("Carregamento finalizado.")

# Função para criar as relações entre escolas e alunos
def criar_relacoes():
    """Cria as relações entre as tabelas escolas e alunos."""
    with engine.connect() as conn:
        # Criar a tabela escolas_alunos
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS escolas_alunos (
                id INTEGER PRIMARY KEY,
                escola_id INTEGER,
                aluno_id INTEGER,
                FOREIGN KEY (escola_id) REFERENCES escolas(id),
                FOREIGN KEY (aluno_id) REFERENCES alunos(id)
            );
        """))
        
        # Inserir dados na tabela escolas_alunos
        conn.execute(text("""
            INSERT INTO escolas_alunos (escola_id, aluno_id)
            SELECT e.id, a.id
            FROM escolas e
            JOIN alunos a ON a.CODESC = e.CODESC;
        """))
        print("Relação criada com sucesso entre escolas e alunos.")

if __name__ == "__main__":
    # Realiza o carregamento de dados
    carregar_dados()
    # Cria as relações
    criar_relacoes()
