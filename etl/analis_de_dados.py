import pandas as pd
import sqlite3
import os
import unicodedata
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(BASE_DIR) == 'etl':
    BASE_DIR = os.path.dirname(BASE_DIR)

path_ranking = os.path.join(BASE_DIR, 'data', 'raw', 'csv', 'ranking_oficial_fundec_2024.csv')
path_repasses = os.path.join(BASE_DIR, 'data', 'raw', 'csv', 'repasses_fundec_2024.csv')
path_municipios_br = os.path.join(BASE_DIR, 'data', 'raw', 'csv', 'municipios-brasil.csv')

processed_dir = os.path.join(BASE_DIR, 'data', 'processed')
os.makedirs(processed_dir, exist_ok=True)
db_path = os.path.join(BASE_DIR, 'banco_hackathon.db')


def normaliza_nome(s):
    nfkd = unicodedata.normalize('NFKD', str(s))
    return ''.join(c for c in nfkd if not unicodedata.combining(c)).upper().strip()


# =========================================================================
# 1. LEITURA DOS DADOS BRUTOS
# =========================================================================

print("--- PROCESSANDO RANKING ---")
df_ranking = pd.read_csv(path_ranking, sep=',', encoding='utf-8')
df_ranking.columns = df_ranking.columns.str.strip().str.replace(' ', '_').str.lower()

print("\n--- PROCESSANDO REPASSES ---")
df_repasses = pd.read_csv(
    path_repasses,
    sep=',',
    encoding='utf-8',
    dtype={'Processo': 'string', 'CNPJ': 'string', 'Empenho': 'string'},
)
df_repasses.columns = df_repasses.columns.str.strip().str.replace(' ', '_').str.lower()

print("COLUNAS REPASSES:", df_repasses.columns.tolist())

print("\n--- LENDO MUNICIPIOS-BRASIL.CSV ---")
df_mun_br = pd.read_csv(path_municipios_br, sep=',', encoding='utf-8')

# =========================================================================
# 2. LIMPEZA E TRATAMENTO DE TIPOS
# =========================================================================

if 'município' in df_repasses.columns:
    df_repasses = df_repasses.dropna(subset=['município']).copy()

if 'data' in df_repasses.columns:
    df_repasses['data'] = pd.to_datetime(df_repasses['data'], errors='coerce')

# --- CORREÇÃO CRÍTICA: conversão de valores monetários ---
# Formato original: "R$ 784.883,72" ou "-R$ 400.000,00"
# Passos: 1) remover R$, 2) strip, 3) remover pontos (separador de milhar),
#         4) trocar vírgula por ponto, 5) remover espaços internos
if 'valor' in df_repasses.columns:
    if df_repasses['valor'].dtype == 'object' or df_repasses['valor'].dtype == 'string':
        df_repasses['valor'] = (
            df_repasses['valor']
            .str.replace('R$', '', regex=False)
            .str.strip()
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
            .str.replace(' ', '', regex=False)
        )
    df_repasses['valor'] = pd.to_numeric(df_repasses['valor'], errors='coerce')

# CNPJ, processo e empenho já foram lidos como dtype='string',
# mas garantimos a limpeza caso tenham vindo com ".0"
for col in ['cnpj', 'processo', 'empenho']:
    if col in df_repasses.columns:
        df_repasses[col] = (
            df_repasses[col]
            .astype(str)
            .str.replace(r'\.0$', '', regex=True)
            .replace(['nan', '<NA>', 'NaN'], pd.NA)
        )

duplicadas = df_repasses.duplicated().sum()
print(f"Duplicidades na base de repasses: {duplicadas}")
df_repasses = df_repasses.drop_duplicates()

valores_negativos = df_repasses[df_repasses['valor'] < 0]
print(f"Registros negativos preservados: {len(valores_negativos)}")
if not valores_negativos.empty:
    valores_negativos.to_csv(
        os.path.join(processed_dir, 'doc_18_valores_negativos.csv'), index=False
    )

# =========================================================================
# 3. CONSTRUÇÃO DE dim_municipio VIA MUNICIPIOS-BRASIL.CSV
# =========================================================================

print("\nGerando dim_municipio (via municipios-brasil.csv)...")

df_mun_br_rs = df_mun_br[df_mun_br['uf'] == 'RS'].copy()
df_mun_br_rs['municipio_norm'] = df_mun_br_rs['municipio'].apply(normaliza_nome)

df_ranking['municipio_norm'] = df_ranking['município'].apply(normaliza_nome)

dim_municipio = pd.merge(
    df_ranking,
    df_mun_br_rs[[
        'municipio_norm', 'codigo_ibge', 'regiao',
        'populacao_2025', 'populacao_censo_2022',
        'pib_2023_mil_reais', 'pib_per_capita_2023_reais',
        'area_km2', 'densidade_hab_km2', 'idhm_2010',
    ]],
    on='municipio_norm',
    how='left',
)
dim_municipio = dim_municipio.drop(columns=['municipio_norm'])

# Converter valor_pago_(r$) de "5958562,42" para float
if 'valor_pago_(r$)' in dim_municipio.columns:
    dim_municipio['valor_pago'] = (
        dim_municipio['valor_pago_(r$)']
        .astype(str)
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
        .str.replace('R$', '', regex=False)
        .str.strip()
    )
    dim_municipio['valor_pago'] = pd.to_numeric(dim_municipio['valor_pago'], errors='coerce')

# Enriquecer com métricas agregadas da fato
print("Enriquecendo dim_municipio com métricas da fato...")
resumo_fato = df_repasses.groupby('município').agg(
    total_repasses=('valor', 'sum'),
    qtd_repasses=('valor', 'count'),
    valor_medio=('valor', 'mean'),
).reset_index()
dim_municipio = pd.merge(dim_municipio, resumo_fato, on='município', how='left')
dim_municipio['total_repasses'] = dim_municipio['total_repasses'].fillna(0)
dim_municipio['qtd_repasses'] = dim_municipio['qtd_repasses'].fillna(0).astype(int)
dim_municipio['valor_medio'] = dim_municipio['valor_medio'].fillna(0)

# chave_municipal: 7 dígitos zero-padded a partir do codigo_ibge
dim_municipio['chave_municipal'] = (
    dim_municipio['codigo_ibge']
    .astype('Int64')
    .astype(str)
    .str.zfill(7)
)

# Reordenar colunas para clareza
ordem_dim = [
    'chave_municipal', 'município', 'codigo_ibge', 'regiao',
    'populacao_2025', 'populacao_censo_2022',
    'idhm_2010', 'pib_per_capita_2023_reais', 'pib_2023_mil_reais',
    'densidade_hab_km2', 'area_km2',
    'valor_pago', 'total_repasses', 'qtd_repasses', 'valor_medio',
]
ordem_dim = [c for c in ordem_dim if c in dim_municipio.columns]
dim_municipio = dim_municipio[ordem_dim]

# Verificar cobertura IBGE
sem_ibge = dim_municipio[dim_municipio['codigo_ibge'].isna()]
if not sem_ibge.empty:
    print(f"ATENÇÃO: {len(sem_ibge)} municípios sem código IBGE: {sem_ibge['município'].tolist()}")
else:
    print(f"Todos os {len(dim_municipio)} municípios associados ao IBGE.")

dim_municipio.to_csv(os.path.join(processed_dir, 'dim_municipio.csv'), index=False)

# =========================================================================
# 4. CONSTRUÇÃO DE fato_repasses
# =========================================================================

print("\nGerando fato_repasses...")

colunas_fato = ['data', 'município', 'processo', 'empenho', 'cnpj', 'credor', 'recurso', 'valor']
colunas_fato = [c for c in colunas_fato if c in df_repasses.columns]
fato_repasses = df_repasses[colunas_fato].copy()

# Trazer chave_municipal da dim_municipio
fato_repasses = pd.merge(
    fato_repasses,
    dim_municipio[['município', 'chave_municipal', 'codigo_ibge']],
    on='município',
    how='left',
)

# Registros sem chave_municipal recebem nulo (não 0000000)
fato_repasses['chave_municipal'] = fato_repasses['chave_municipal'].where(
    fato_repasses['chave_municipal'].notna(), other=pd.NA
)

if 'data' in fato_repasses.columns:
    fato_repasses['data'] = fato_repasses['data'].dt.strftime('%Y-%m-%d')

# Reordenar: data e chave_municipal primeiro, depois atributos
ordem_fato = ['data', 'chave_municipal', 'processo', 'empenho', 'cnpj', 'credor', 'recurso', 'valor']
ordem_fato = [c for c in ordem_fato if c in fato_repasses.columns]
fato_repasses = fato_repasses[ordem_fato]

fato_repasses.to_csv(os.path.join(processed_dir, 'fato_repasses.csv'), index=False)

# =========================================================================
# 5. CONSTRUÇÃO DE dim_calendario
# =========================================================================

print("Gerando dim_calendario...")
df_datas = pd.to_datetime(fato_repasses['data'], errors='coerce')
dim_calendario = pd.DataFrame({'data': df_datas.dropna().unique()})
dim_calendario['ano'] = pd.to_datetime(dim_calendario['data']).dt.year
dim_calendario['mes'] = pd.to_datetime(dim_calendario['data']).dt.month
dim_calendario.to_csv(os.path.join(processed_dir, 'dim_calendario.csv'), index=False)

# =========================================================================
# 6. CONCILIAÇÃO
# =========================================================================

print("\n--- CONCILIAÇÃO ---")
total_fato = fato_repasses['valor'].sum()
print(f"Total Detalhado (Fato): R$ {total_fato:,.2f}")

if 'valor_pago' in dim_municipio.columns:
    total_ranking = dim_municipio['valor_pago'].sum()
    diferenca = total_fato - total_ranking
    print(f"Total Oficial (Ranking): R$ {total_ranking:,.2f}")
    print(f"Diferença: R$ {diferenca:,.2f}")

    # Gerar CSV de conciliação por município (usa dim_municipio como referência)
    conciliacao = dim_municipio[['município', 'chave_municipal', 'valor_pago']].copy()
    soma_fato = fato_repasses.groupby('chave_municipal')['valor'].sum().reset_index()
    soma_fato.columns = ['chave_municipal', 'total_fato']
    conciliacao = pd.merge(conciliacao, soma_fato, on='chave_municipal', how='left')
    conciliacao['total_fato'] = conciliacao['total_fato'].fillna(0)
    conciliacao['diferenca'] = conciliacao['total_fato'] - conciliacao['valor_pago']
    conciliacao = conciliacao.sort_values('diferenca')
    conciliacao.to_csv(os.path.join(processed_dir, 'conciliacao.csv'), index=False)
    print(f"Conciliação salva em: {os.path.join(processed_dir, 'conciliacao.csv')}")

# =========================================================================
# 7. RELATÓRIO DE INCONSISTÊNCIAS
# =========================================================================

print("\n--- RELATÓRIO DE INCONSISTÊNCIAS ---")
inconsistencias = []

# Municípios fato sem chave_municipal
sem_chave = fato_repasses[fato_repasses['chave_municipal'].isna()]
if not sem_chave.empty:
    # Reter municipio original no fato para o relatório
    fato_com_mun = df_repasses[['município', 'data']].copy()
    fato_com_mun['data'] = fato_com_mun['data'].dt.strftime('%Y-%m-%d')
    sem_chave_info = sem_chave.merge(fato_com_mun, left_index=True, right_index=True, how='left')
    for _, row in sem_chave_info.iterrows():
        inconsistencias.append({
            'tipo': 'fato_sem_chave_municipal',
            'municipio': row.get('município', ''),
            'detalhe': f'Registro na data {row.get("data", "")} sem chave_municipal associada',
        })

# Municípios ranking sem código IBGE na dim
if not sem_ibge.empty:
    for _, row in sem_ibge.iterrows():
        inconsistencias.append({
            'tipo': 'ranking_sem_ibge',
            'município': row.get('município', ''),
            'detalhe': 'Município no ranking sem código IBGE em municipios-brasil.csv',
        })

# Valores nulos na fato
nulos_valor = fato_repasses[fato_repasses['valor'].isna()]
if not nulos_valor.empty:
    for _, row in nulos_valor.iterrows():
        inconsistencias.append({
            'tipo': 'valor_nulo',
            'municipio': row.get('município', ''),
            'detalhe': f'Valor nulo na data {row.get("data", "")}',
        })

if inconsistencias:
    df_inc = pd.DataFrame(inconsistencias)
    df_inc.to_csv(os.path.join(processed_dir, 'inconsistencias.csv'), index=False)
    print(f"Inconsistências encontradas: {len(inconsistencias)}")
    print(f"Salvo em: {os.path.join(processed_dir, 'inconsistencias.csv')}")
else:
    print("Nenhuma inconsistência encontrada.")

# =========================================================================
# 8. RELATÓRIO DE VALIDAÇÃO
# =========================================================================

print("\n--- RELATÓRIO DE VALIDAÇÃO ---")
validacao = {
    'metrica': [
        'total_registros_fato',
        'total_municipios_dim',
        'negativos_preservados',
        'negativos_esperados',
        'soma_total_fato',
        'soma_total_ranking',
        'diferenca_conciliacao',
        'municipios_com_ibge',
        'municipios_sem_ibge',
        'fato_com_chave_municipal',
        'fato_sem_chave_municipal',
        'duplicatas_exatas',
    ],
    'valor': [
        len(fato_repasses),
        len(dim_municipio),
        len(valores_negativos),
        18,
        round(total_fato, 2),
        round(total_ranking, 2) if 'valor_pago' in dim_municipio.columns else None,
        round(diferenca, 2) if 'valor_pago' in dim_municipio.columns else None,
        int(dim_municipio['codigo_ibge'].notna().sum()),
        int(dim_municipio['codigo_ibge'].isna().sum()),
        int(fato_repasses['chave_municipal'].notna().sum()),
        int(fato_repasses['chave_municipal'].isna().sum()),
        duplicadas,
    ],
}
df_validacao = pd.DataFrame(validacao)
df_validacao.to_csv(os.path.join(processed_dir, 'relatorio_validacao.csv'), index=False)

for _, row in df_validacao.iterrows():
    print(f"  {row['metrica']}: {row['valor']}")

print(f"\nRelatório de validação salvo em: {os.path.join(processed_dir, 'relatorio_validacao.csv')}")

# =========================================================================
# 9. EXPORTAÇÃO SQLITE
# =========================================================================

conn = sqlite3.connect(db_path)
df_ranking.to_sql('dim_ranking', conn, if_exists='replace', index=False)
dim_municipio.to_sql('dim_municipio', conn, if_exists='replace', index=False)
fato_repasses.to_sql('fato_repasses', conn, if_exists='replace', index=False)
dim_calendario.to_sql('dim_calendario', conn, if_exists='replace', index=False)
conn.close()

print(f"\nCSVs prontos para o Qlik Sense em: {processed_dir}")
print(f"  - fato_repasses.csv (com chave_municipal)")
print(f"  - dim_municipio.csv (com indicadores IBGE, IDH-M, PIB)")
print(f"  - dim_calendario.csv")
print(f"  - conciliacao.csv")
print(f"  - inconsistencias.csv")
print(f"  - relatorio_validacao.csv")
print(f"\nBanco SQLite atualizado em: {db_path}")
