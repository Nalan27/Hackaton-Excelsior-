import pandas as pd
import sqlite3
import os
import numpy as np

# Descobre o caminho raiz do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(BASE_DIR) == 'etl':
    BASE_DIR = os.path.dirname(BASE_DIR)

path_ranking = os.path.join(BASE_DIR, 'data', 'raw','csv', 'ranking_oficial_fundec_2024.csv')
path_repasses = os.path.join(BASE_DIR, 'data', 'raw','csv', 'repasses_fundec_2024.csv')

# Caminho para a base do IBGE (Necessário para a população e indicadores)
path_ibge = os.path.join(BASE_DIR, 'data', 'raw','csv', 'populacao_rs_2024.csv') 

# Pasta de saída para o Qlik
processed_dir = os.path.join(BASE_DIR, 'data', 'processed')
os.makedirs(processed_dir, exist_ok=True)

db_path = os.path.join(BASE_DIR, 'banco_hackathon.db')

print("--- PROCESSANDO RANKING ---")
df_ranking = pd.read_csv(path_ranking, sep=',', encoding='utf-8')
df_ranking.columns = df_ranking.columns.str.strip().str.replace(' ', '_').str.lower()

print("\n--- PROCESSANDO REPASSES ---")
df_repasses = pd.read_csv(path_repasses, sep=',', encoding='utf-8')
df_repasses.columns = df_repasses.columns.str.strip().str.replace(' ', '_').str.lower()

print("COLUNAS APÓS LIMPEZA:", df_repasses.columns.tolist())


# Remove linhas sem município
if 'município' in df_repasses.columns:
    df_repasses_limpo = df_repasses.dropna(subset=['município']).copy()
else:
    df_repasses_limpo = df_repasses.copy()

# 1. TRATAMENTO DE TIPOS E DADOS (CHECKLIST)

# Manter Data como data
if 'data' in df_repasses_limpo.columns:
    df_repasses_limpo['data'] = pd.to_datetime(df_repasses_limpo['data'], errors='coerce')

# Manter Valor como decimal com sinal
if 'valor' in df_repasses_limpo.columns:
    # Se o CSV veio como texto (ex: "R$ 784883,72"), corrige formatação
    if df_repasses_limpo['valor'].dtype == 'object' or df_repasses_limpo['valor'].dtype == 'string':
        df_repasses_limpo['valor'] = df_repasses_limpo['valor'].str.replace('R$', '', regex=False).str.strip()
        df_repasses_limpo['valor'] = df_repasses_limpo['valor'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
    
    df_repasses_limpo['valor'] = pd.to_numeric(df_repasses_limpo['valor'], errors='coerce')

# Tratar CNPJ, processo e empenho como texto
colunas_texto = ['cnpj', 'processo', 'empenho']
for col in colunas_texto:
    if col in df_repasses_limpo.columns:
        # Regex remove o ".0" no final caso o pandas tenha lido como float originalmente
        df_repasses_limpo[col] = df_repasses_limpo[col].astype(str).str.replace(r'\.0$', '', regex=True)
        df_repasses_limpo[col] = df_repasses_limpo[col].replace(['nan', '<NA>', 'NaN'], '')

# Verificar duplicidades
duplicadas = df_repasses_limpo.duplicated().sum()
print(f"Duplicidades na base de repasses: {duplicadas}")
df_repasses_limpo = df_repasses_limpo.drop_duplicates()

# Preservar e documentar os 18 valores negativos
valores_negativos = df_repasses_limpo[df_repasses_limpo['valor'] < 0]
if not valores_negativos.empty:
    valores_negativos.to_csv(os.path.join(processed_dir, 'doc_18_valores_negativos.csv'), index=False)
    print(f"Registros negativos salvos: {len(valores_negativos)} (Documentação)")

# 2. MODELAGEM STAR SCHEMA PARA O QLIK

# Gerar dim_calendario.csv
print("\nGerando dim_calendario...")
dim_calendario = pd.DataFrame({'data': df_repasses_limpo['data'].dropna().unique()})
dim_calendario['ano'] = dim_calendario['data'].dt.year
dim_calendario['mes'] = dim_calendario['data'].dt.month
dim_calendario.to_csv(os.path.join(processed_dir, 'dim_calendario.csv'), index=False)

# Gerar dim_municipio.csv (Com IBGE e Indicadores)
print("Gerando dim_municipio...")
dim_municipio = df_ranking.copy() 

if os.path.exists(path_ibge):
    print("Processando base de população...")
    colunas_ibge = ['tipo', 'cod_ibge', 'nome_municipio', 'populacao', 'unidade']
    
    df_ibge = pd.read_csv(
        path_ibge, 
        sep=';',              # Volta a ser ponto e vírgula
        encoding='utf-8', 
        names=colunas_ibge, 
        header=None,
        skiprows=2,           # Pula as 2 primeiras linhas de metadados (título e subtítulo)
        quotechar='"',
        on_bad_lines='skip'   # Pula qualquer linha com erro de formatação para não travar o script
    )
    
    # 2. Padroniza a coluna do Ranking (tira espaços e joga pra maiúsculo)
    dim_municipio['municipio_chave'] = dim_municipio['município'].astype(str).str.upper().str.strip()
    
    # 3. O PULO DO GATO: Remove o " (RS)" e padroniza a cidade do IBGE
    df_ibge['municipio_chave'] = df_ibge['nome_municipio'].astype(str).str.replace(' (RS)', '', regex=False)
    df_ibge['municipio_chave'] = df_ibge['municipio_chave'].str.upper().str.strip()
    
    # Garante que a população seja um número inteiro
    df_ibge['populacao'] = pd.to_numeric(df_ibge['populacao'], errors='coerce')
    
    # 4. Faz o cruzamento trazendo SÓ o que importa (Código IBGE e População)
    dim_municipio = pd.merge(
        dim_municipio, 
        df_ibge[['municipio_chave', 'cod_ibge', 'populacao']], 
        on='municipio_chave', 
        how='left'
    )
    
    # Remove a coluna temporária de cruzamento
    dim_municipio = dim_municipio.drop(columns=['municipio_chave'])

# Enriquecer dim_municipio com métricas da fato de repasses
print("Enriquecendo dim_municipio com métricas da fato...")
resumo_fato = df_repasses_limpo.groupby('município').agg(
    total_repasses=('valor', 'sum'),
    qtd_repasses=('valor', 'count'),
    valor_medio=('valor', 'mean')
).reset_index()
dim_municipio = pd.merge(dim_municipio, resumo_fato, on='município', how='left')
dim_municipio['total_repasses'] = dim_municipio['total_repasses'].fillna(0)
dim_municipio['qtd_repasses'] = dim_municipio['qtd_repasses'].fillna(0).astype(int)
dim_municipio['valor_medio'] = dim_municipio['valor_medio'].fillna(0)

# Verificar municípios não associados
municipios_fato = set(df_repasses_limpo['município'].dropna())
municipios_dim = set(dim_municipio['município'].dropna())
nao_associados = municipios_fato - municipios_dim
if nao_associados:
    print(f"ATENÇÃO: {len(nao_associados)} municípios da Fato sem associação (IBGE/Ranking): {nao_associados}")

dim_municipio.to_csv(os.path.join(processed_dir, 'dim_municipio.csv'), index=False)

# Gerar fato_repasses.csv
print("Gerando fato_repasses...")
# Deixa só as chaves de ligação (data e município) e colunas essenciais
colunas_fato = ['data', 'município', 'processo', 'empenho', 'cnpj', 'credor', 'recurso', 'valor']
# Filtra apenas as colunas que realmente existem no DF
colunas_fato = [c for c in colunas_fato if c in df_repasses_limpo.columns]

fato_repasses = df_repasses_limpo[colunas_fato].copy()

# Adicionar cod_ibge e chave_municipal via merge com dim_municipio
if 'cod_ibge' in dim_municipio.columns:
    fato_repasses = pd.merge(
        fato_repasses,
        dim_municipio[['município', 'cod_ibge']],
        on='município',
        how='left'
    )
    # Preencher cod_ibge ausentes com 0 e criar chave_municipal com padding
    fato_repasses['cod_ibge'] = fato_repasses['cod_ibge'].fillna(0).astype(int)
    fato_repasses['chave_municipal'] = fato_repasses['cod_ibge'].apply(lambda x: str(x).zfill(7))

# Formatar data como YYYY-MM-DD antes de salvar CSV
if 'data' in fato_repasses.columns:
    fato_repasses['data'] = fato_repasses['data'].dt.strftime('%Y-%m-%d')

fato_repasses.to_csv(os.path.join(processed_dir, 'fato_repasses.csv'), index=False)

# 3. CONCILIAÇÃO

print("\n--- CONCILIAÇÃO ---")
total_fato = fato_repasses['valor'].sum()
print(f"Total Detalhado (Fato): R$ {total_fato:,.2f}")
# Substitua 'valor_total' pela coluna de valor do seu df_ranking para checar a diferença
coluna_valor_ranking = 'valor_pago_(r$)'
if coluna_valor_ranking in df_ranking.columns:
    total_ranking = pd.to_numeric(
        df_ranking[coluna_valor_ranking].str.replace('.', '', regex=False)
                                         .str.replace(',', '.', regex=False)
                                         .str.replace('R$', '', regex=False).str.strip(),
        errors='coerce'
    ).sum()
    diferenca = total_fato - total_ranking
    print(f"Total Oficial (Ranking): R$ {total_ranking:,.2f}")
    print(f"Diferença: R$ {diferenca:,.2f}")

# ==========================================
# 4. SALVAR NO SQLITE 
# ==========================================
# (Mantive isso pois pode ser útil para alguma API em FastAPI que vocês façam depois)
conn = sqlite3.connect(db_path)
df_ranking.to_sql('dim_ranking', conn, if_exists='replace', index=False)
dim_municipio.to_sql('dim_municipio', conn, if_exists='replace', index=False)
fato_repasses.to_sql('fato_repasses', conn, if_exists='replace', index=False)
dim_calendario.to_sql('dim_calendario', conn, if_exists='replace', index=False)
conn.close()

print(f"\nCSV's prontos para o Qlik Sense em: {processed_dir}")
print(f"  - fato_repasses.csv (com chave_municipal)")
print(f"  - dim_municipio.csv (com métricas da fato)")
print(f"  - dim_calendario.csv")
print(f"\nBanco SQLite atualizado em: {db_path}")