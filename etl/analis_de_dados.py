import pandas as pd
import sqlite3
import os

# Descobre o caminho raiz do projeto automaticamente baseado na localização deste script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.basename(BASE_DIR) == 'etl':
    BASE_DIR = os.path.dirname(BASE_DIR)

path_ranking = os.path.join(BASE_DIR, 'data', 'raw', 'ranking_oficial_fundec_2024.csv')
path_repasses = os.path.join(BASE_DIR, 'data', 'raw', 'repasses_fundec_2024.csv')
db_path = os.path.join(BASE_DIR, 'banco_hackathon.db')

print("--- PROCESSANDO RANKING ---")

df_ranking = pd.read_csv(path_ranking, sep=';', encoding='utf-8')
df_ranking.columns = df_ranking.columns.str.strip().str.replace(' ', '_').str.lower()

print(f"Shape Ranking: {df_ranking.shape}")
print(df_ranking.head(2))


print("\n--- PROCESSANDO REPASSES ---")
df_repasses = pd.read_csv(path_repasses, sep=';', encoding='utf-8')
df_repasses.columns = df_repasses.columns.str.strip().str.replace(' ', '_').str.lower()

print(f"Shape Repasses: {df_repasses.shape}")
print(df_repasses.head(2))


if 'município' in df_repasses.columns:
    df_repasses_limpo = df_repasses.dropna(subset=['município']).copy()
else:
    df_repasses_limpo = df_repasses.copy()


if 'data' in df_repasses_limpo.columns:
    df_repasses_limpo['data'] = pd.to_datetime(df_repasses_limpo['data'], errors='coerce')


colunas_ids = ['data', 'processo', 'empenho', 'cnpj', 'credor', 'município', 'recurso', 'valor']
for col in colunas_ids:
    if col in df_repasses_limpo.columns:
        df_repasses_limpo[col] = df_repasses_limpo[col].astype('Int64').astype(str).replace('<NA>', '')


conn = sqlite3.connect(db_path)

# Salva as duas tabelas separadamente no SQLite
df_ranking.to_sql('dim_ranking', conn, if_exists='replace', index=False)
df_repasses_limpo.to_sql('fato_repasses', conn, if_exists='replace', index=False)

conn.close()
print(f"\nBanco SQLite atualizado com sucesso em: {db_path}")