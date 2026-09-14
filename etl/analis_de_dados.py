import pandas as pd
import sqlite3
import os
import unicodedata
import csv

from metricas_repasses import calcular_intervalo_primeiro_repasse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(BASE_DIR) == 'etl':
    BASE_DIR = os.path.dirname(BASE_DIR)

path_ranking = os.path.join(BASE_DIR, 'data', 'raw', 'csv', 'ranking_oficial_fundec_2024.csv')
path_repasses = os.path.join(BASE_DIR, 'data', 'raw', 'csv', 'repasses_fundec_2024.csv')
path_municipios_br = os.path.join(BASE_DIR, 'data', 'raw', 'csv', 'municipios-brasil.csv')
path_populacao_rs_2024 = os.path.join(
    BASE_DIR, 'data', 'raw', 'csv', 'populacao_rs_2024.csv'
)

processed_dir = os.path.join(BASE_DIR, 'data', 'processed')
os.makedirs(processed_dir, exist_ok=True)
db_path = os.path.join(BASE_DIR, 'banco_hackathon.db')

EXPECTED_TOTAL_REGISTROS = 658
EXPECTED_TOTAL_MUNICIPIOS = 334
EXPECTED_NEGATIVOS = 18
EXPECTED_TOTAL_FATO = 288_699_999.97
EXPECTED_TOTAL_RANKING = 289_176_004.25
EXPECTED_DIFERENCA = -476_004.28
EXPECTED_INTERVALOS = 334
EXPECTED_MUNICIPIOS_RS = 497
DATA_MARCO_ADOTADO = '2024-04-24'
TOLERANCIA_MONETARIA = 0.01


def normaliza_nome(s):
    if pd.isna(s):
        return pd.NA
    nfkd = unicodedata.normalize('NFKD', str(s))
    sem_acentos = ''.join(c for c in nfkd if not unicodedata.combining(c))
    return ' '.join(sem_acentos.upper().split())


def cria_chave_municipal(codigo_ibge):
    if pd.isna(codigo_ibge):
        return pd.NA
    return f'{int(codigo_ibge):07d}'


def exige_colunas(df, colunas, fonte):
    ausentes = sorted(set(colunas) - set(df.columns))
    if ausentes:
        raise ValueError(f'Colunas ausentes em {fonte}: {", ".join(ausentes)}')


def ler_populacao_rs_2024(caminho):
    """Le as linhas municipais da exportacao bruta da SIDRA Tabela 6579."""
    registros = []
    with open(caminho, encoding='utf-8-sig', newline='') as arquivo:
        for linha in csv.reader(arquivo, delimiter=';'):
            if len(linha) < 5 or linha[0] != 'MU':
                continue

            nome_ibge = linha[2].strip()
            if nome_ibge.endswith(' (RS)'):
                nome_ibge = nome_ibge[:-5]

            registros.append({
                'codigo_ibge': int(linha[1]),
                'municipio_ibge_2024': nome_ibge,
                'populacao_2024': int(linha[3]),
                'unidade_populacao_2024': linha[4].strip(),
            })

    populacao = pd.DataFrame(registros)
    if len(populacao) != EXPECTED_MUNICIPIOS_RS:
        raise ValueError(
            'Cobertura inesperada na populacao SIDRA 2024: '
            f'{len(populacao)} municipios; esperado {EXPECTED_MUNICIPIOS_RS}'
        )
    if populacao['codigo_ibge'].duplicated().any():
        raise ValueError('Codigos IBGE duplicados na populacao SIDRA 2024')
    if populacao['populacao_2024'].le(0).any():
        raise ValueError('Populacao SIDRA 2024 nula ou nao positiva')
    if set(populacao['unidade_populacao_2024']) != {'Pessoas'}:
        raise ValueError('Unidade inesperada na populacao SIDRA 2024')

    return populacao.drop(columns='unidade_populacao_2024')


def exportar_sqlite(
    df_ranking,
    dim_municipio,
    fato_repasses,
    dim_calendario,
    intervalo_primeiro_repasse,
):
    """Exporta o modelo com PKs e FKs efetivamente declaradas no SQLite."""
    with sqlite3.connect(db_path) as conn:
        conn.execute('PRAGMA foreign_keys = ON')
        conn.execute('DROP TABLE IF EXISTS intervalo_primeiro_repasse')
        conn.execute('DROP TABLE IF EXISTS fato_repasses')
        conn.execute('DROP TABLE IF EXISTS dim_calendario')
        conn.execute('DROP TABLE IF EXISTS dim_municipio')
        conn.execute('DROP TABLE IF EXISTS dim_ranking')

        conn.execute('''
            CREATE TABLE dim_municipio (
                chave_municipal TEXT PRIMARY KEY,
                "município" TEXT NOT NULL,
                codigo_ibge INTEGER NOT NULL UNIQUE,
                municipio_ibge_2024 TEXT NOT NULL,
                localizacao_mapa TEXT NOT NULL UNIQUE,
                regiao TEXT,
                populacao_2024 INTEGER NOT NULL,
                populacao_2025 INTEGER,
                populacao_censo_2022 REAL,
                idhm_2010 REAL,
                pib_per_capita_2023_reais REAL,
                pib_2023_mil_reais REAL,
                densidade_hab_km2 REAL,
                area_km2 REAL,
                valor_pago REAL,
                total_repasses REAL,
                valor_por_pessoa_2024 REAL NOT NULL,
                qtd_repasses INTEGER,
                valor_medio REAL
            )
        ''')
        conn.execute('''
            CREATE TABLE dim_calendario (
                data TEXT PRIMARY KEY,
                ano INTEGER NOT NULL,
                trimestre TEXT NOT NULL,
                mes INTEGER NOT NULL,
                mes_nome TEXT NOT NULL,
                ano_mes TEXT NOT NULL,
                ano_mes_ordem INTEGER NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE fato_repasses (
                data TEXT NOT NULL,
                chave_municipal TEXT NOT NULL,
                processo TEXT,
                empenho TEXT,
                cnpj TEXT,
                credor TEXT,
                recurso TEXT,
                valor REAL NOT NULL,
                FOREIGN KEY (data) REFERENCES dim_calendario(data),
                FOREIGN KEY (chave_municipal)
                    REFERENCES dim_municipio(chave_municipal)
            )
        ''')
        conn.execute('''
            CREATE TABLE intervalo_primeiro_repasse (
                chave_municipal TEXT PRIMARY KEY,
                data_marco_adotado TEXT,
                tipo_marco_adotado TEXT NOT NULL,
                fonte_marco_adotado TEXT NOT NULL,
                data_primeiro_repasse_elegivel TEXT,
                intervalo_desde_marco_adotado_dias INTEGER,
                status_intervalo TEXT NOT NULL,
                criterio_primeiro_repasse TEXT NOT NULL,
                qtd_estornos_ignorados INTEGER NOT NULL,
                FOREIGN KEY (chave_municipal)
                    REFERENCES dim_municipio(chave_municipal)
            )
        ''')

        dim_municipio.to_sql('dim_municipio', conn, if_exists='append', index=False)
        dim_calendario.to_sql('dim_calendario', conn, if_exists='append', index=False)
        fato_repasses.to_sql('fato_repasses', conn, if_exists='append', index=False)
        intervalo_primeiro_repasse.to_sql(
            'intervalo_primeiro_repasse', conn, if_exists='append', index=False
        )
        df_ranking.to_sql('dim_ranking', conn, if_exists='replace', index=False)


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

print("\n--- LENDO POPULACAO SIDRA 2024 ---")
df_populacao_rs_2024 = ler_populacao_rs_2024(path_populacao_rs_2024)

exige_colunas(df_ranking, {'município', 'valor_pago_(r$)'}, path_ranking)
exige_colunas(
    df_repasses,
    {'data', 'processo', 'recurso', 'empenho', 'cnpj', 'credor', 'município', 'valor'},
    path_repasses,
)
exige_colunas(
    df_mun_br,
    {
        'municipio', 'uf', 'codigo_ibge', 'regiao', 'populacao_2025',
        'populacao_censo_2022', 'pib_2023_mil_reais',
        'pib_per_capita_2023_reais', 'area_km2', 'densidade_hab_km2',
        'idhm_2010',
    },
    path_municipios_br,
)

# =========================================================================
# 2. LIMPEZA E TRATAMENTO DE TIPOS
# =========================================================================

municipios_ausentes_origem = df_repasses[
    df_repasses['município'].isna()
    | df_repasses['município'].astype('string').str.strip().eq('').fillna(False)
].copy()

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
df_repasses['municipio_norm'] = df_repasses['município'].apply(normaliza_nome)

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
dim_municipio = pd.merge(
    dim_municipio,
    df_populacao_rs_2024,
    on='codigo_ibge',
    how='left',
    validate='many_to_one',
)
dim_municipio['localizacao_mapa'] = (
    dim_municipio['municipio_ibge_2024'] + ', Rio Grande do Sul, Brasil'
)
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
resumo_fato = df_repasses.groupby('municipio_norm').agg(
    total_repasses=('valor', 'sum'),
    qtd_repasses=('valor', 'count'),
    valor_medio=('valor', 'mean'),
).reset_index()
dim_municipio = pd.merge(dim_municipio, resumo_fato, on='municipio_norm', how='left')
dim_municipio['total_repasses'] = dim_municipio['total_repasses'].fillna(0)
dim_municipio['qtd_repasses'] = dim_municipio['qtd_repasses'].fillna(0).astype(int)
dim_municipio['valor_medio'] = dim_municipio['valor_medio'].fillna(0)
dim_municipio['valor_por_pessoa_2024'] = (
    dim_municipio['total_repasses'] / dim_municipio['populacao_2024']
)

# chave_municipal: 7 dígitos zero-padded a partir do codigo_ibge
dim_municipio['chave_municipal'] = (
    dim_municipio['codigo_ibge']
    .apply(cria_chave_municipal)
    .astype('string')
)
mapa_municipios = dim_municipio[
    ['municipio_norm', 'chave_municipal', 'codigo_ibge']
].copy()

# Reordenar colunas para clareza
ordem_dim = [
    'chave_municipal', 'município', 'codigo_ibge',
    'municipio_ibge_2024', 'localizacao_mapa', 'regiao',
    'populacao_2024', 'populacao_2025', 'populacao_censo_2022',
    'idhm_2010', 'pib_per_capita_2023_reais', 'pib_2023_mil_reais',
    'densidade_hab_km2', 'area_km2',
    'valor_pago', 'total_repasses', 'valor_por_pessoa_2024',
    'qtd_repasses', 'valor_medio',
]
ordem_dim = [c for c in ordem_dim if c in dim_municipio.columns]
dim_municipio = dim_municipio[ordem_dim]

# Verificar cobertura IBGE
sem_ibge = dim_municipio[dim_municipio['codigo_ibge'].isna()]
if not sem_ibge.empty:
    print(f"ATENÇÃO: {len(sem_ibge)} municípios sem código IBGE: {sem_ibge['município'].tolist()}")
else:
    print(f"Todos os {len(dim_municipio)} municípios associados ao IBGE.")

sem_populacao_2024 = dim_municipio[dim_municipio['populacao_2024'].isna()]
localizacoes_duplicadas = int(dim_municipio['localizacao_mapa'].duplicated().sum())
if sem_populacao_2024.empty:
    print(
        f"Todos os {len(dim_municipio)} municipios possuem populacao SIDRA 2024."
    )
else:
    print(
        f"ATENCAO: {len(sem_populacao_2024)} municipios sem populacao SIDRA 2024."
    )

dim_municipio.to_csv(os.path.join(processed_dir, 'dim_municipio.csv'), index=False)

# =========================================================================
# 4. CONSTRUÇÃO DE fato_repasses
# =========================================================================

print("\nGerando fato_repasses...")

colunas_fato = [
    'data', 'município', 'municipio_norm', 'processo', 'empenho',
    'cnpj', 'credor', 'recurso', 'valor',
]
colunas_fato = [c for c in colunas_fato if c in df_repasses.columns]
fato_repasses = df_repasses[colunas_fato].copy()

# Trazer chave_municipal da dim_municipio
fato_repasses = pd.merge(
    fato_repasses,
    mapa_municipios,
    on='municipio_norm',
    how='left',
)

# Registros sem chave_municipal recebem nulo (não 0000000)
fato_repasses['chave_municipal'] = fato_repasses['chave_municipal'].where(
    fato_repasses['chave_municipal'].notna(), other=pd.NA
)

sem_chave_info = fato_repasses.loc[
    fato_repasses['chave_municipal'].isna(),
    ['município', 'data', 'processo'],
].copy()

if 'data' in fato_repasses.columns:
    fato_repasses['data'] = fato_repasses['data'].dt.strftime('%Y-%m-%d')

# Reordenar: data e chave_municipal primeiro, depois atributos
ordem_fato = ['data', 'chave_municipal', 'processo', 'empenho', 'cnpj', 'credor', 'recurso', 'valor']
ordem_fato = [c for c in ordem_fato if c in fato_repasses.columns]
fato_repasses = fato_repasses[ordem_fato]

fato_repasses.to_csv(os.path.join(processed_dir, 'fato_repasses.csv'), index=False)

# =========================================================================
# 5. INTERVALO DESDE O MARCO ADOTADO ATÉ O PRIMEIRO REPASSE
# =========================================================================

print("Gerando intervalo_primeiro_repasse...")

# O Decreto Estadual nº 57.604/2024 vincula os repasses excepcionais do
# FUNDEC/RS aos eventos climáticos cujo período estadual iniciou em
# 24/04/2024. Esta data não representa necessariamente o impacto local em
# cada município; é somente o marco documental comum adotado para a métrica.
marcos_temporais = dim_municipio[['chave_municipal']].copy()
marcos_temporais['data_marco_adotado'] = DATA_MARCO_ADOTADO
marcos_temporais['tipo_marco_adotado'] = (
    'início do período estadual dos eventos climáticos'
)
marcos_temporais['fonte_marco_adotado'] = (
    'Decreto Estadual RS nº 57.604/2024, art. 1º'
)

intervalo_primeiro_repasse = calcular_intervalo_primeiro_repasse(
    fato_repasses,
    marcos_temporais,
)

for coluna_data in [
    'data_marco_adotado',
    'data_primeiro_repasse_elegivel',
]:
    intervalo_primeiro_repasse[coluna_data] = (
        intervalo_primeiro_repasse[coluna_data].dt.strftime('%Y-%m-%d')
    )

intervalo_primeiro_repasse.to_csv(
    os.path.join(processed_dir, 'intervalo_primeiro_repasse.csv'),
    index=False,
)

# =========================================================================
# 6. CONSTRUÇÃO DE dim_calendario
# =========================================================================

print("Gerando dim_calendario...")

# Interpreta as datas da fato. errors='raise' interrompe o ETL se houver
# alguma data inválida.
datas_fato = pd.to_datetime(
    fato_repasses['data'],
    format='%Y-%m-%d',
    errors='raise',
)

# Cria uma linha para cada dia entre a primeira e a última movimentação.
dim_calendario = pd.DataFrame({
    'data': pd.date_range(
        start=datas_fato.min(),
        end=datas_fato.max(),
        freq='D',
    )
})

nomes_meses = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro',
}

dim_calendario['ano'] = dim_calendario['data'].dt.year
dim_calendario['trimestre'] = (
    'T' + dim_calendario['data'].dt.quarter.astype(str)
)
dim_calendario['mes'] = dim_calendario['data'].dt.month
dim_calendario['mes_nome'] = dim_calendario['mes'].map(nomes_meses)
dim_calendario['ano_mes'] = dim_calendario['data'].dt.strftime('%Y-%m')

# Essa coluna permite ordenar ano-mês corretamente no Qlik.
dim_calendario['ano_mes_ordem'] = (
    dim_calendario['ano'] * 100 + dim_calendario['mes']
)

# Exporta a chave de data no mesmo formato utilizado pela fato.
dim_calendario['data'] = dim_calendario['data'].dt.strftime('%Y-%m-%d')

dim_calendario.to_csv(
    os.path.join(processed_dir, 'dim_calendario.csv'),
    index=False,
)

# =========================================================================
# 7. CONCILIAÇÃO
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
    conciliacao['diferenca'] = (
        conciliacao['total_fato'] - conciliacao['valor_pago']
    ).round(2)
    conciliacao = conciliacao.sort_values('diferenca')
    conciliacao.to_csv(os.path.join(processed_dir, 'conciliacao.csv'), index=False)
    print(f"Conciliação salva em: {os.path.join(processed_dir, 'conciliacao.csv')}")

# =========================================================================
# 8. RELATÓRIO DE INCONSISTÊNCIAS
# =========================================================================

print("\n--- RELATÓRIO DE INCONSISTÊNCIAS ---")
inconsistencias = []

for _, row in intervalo_primeiro_repasse[
    intervalo_primeiro_repasse['status_intervalo'] != 'ok'
].iterrows():
    inconsistencias.append({
        'severidade': 'AVISO',
        'tipo': row['status_intervalo'],
        'municipio': '',
        'detalhe': (
            f'Chave municipal {row["chave_municipal"]} sem intervalo publicável'
        ),
    })

for _, row in municipios_ausentes_origem.iterrows():
    inconsistencias.append({
        'severidade': 'ERRO',
        'tipo': 'fato_sem_municipio',
        'municipio': '',
        'detalhe': f'Processo {row.get("processo", "")} sem município informado',
    })

for _, row in sem_chave_info.iterrows():
    data = row.get('data')
    data = data.strftime('%Y-%m-%d') if pd.notna(data) else ''
    inconsistencias.append({
        'severidade': 'ERRO',
        'tipo': 'fato_sem_chave_municipal',
        'municipio': row.get('município', ''),
        'detalhe': f'Registro na data {data} sem chave_municipal associada',
    })

# Municípios ranking sem código IBGE na dim
for _, row in sem_ibge.iterrows():
    inconsistencias.append({
        'severidade': 'ERRO',
        'tipo': 'ranking_sem_ibge',
        'municipio': row.get('município', ''),
        'detalhe': 'Município no ranking sem código IBGE em municipios-brasil.csv',
    })

# Valores nulos na fato
nulos_valor = fato_repasses[fato_repasses['valor'].isna()]
for _, row in nulos_valor.iterrows():
    inconsistencias.append({
        'severidade': 'ERRO',
        'tipo': 'valor_nulo',
        'municipio': '',
        'detalhe': f'Valor nulo na data {row.get("data", "")}',
    })

datas_invalidas = int(df_repasses['data'].isna().sum())
for _, row in df_repasses[df_repasses['data'].isna()].iterrows():
    inconsistencias.append({
        'severidade': 'ERRO',
        'tipo': 'data_invalida',
        'municipio': row.get('município', ''),
        'detalhe': f'Data inválida no processo {row.get("processo", "")}',
    })

# Pinto Bandeira não possui IDH-M 2010 na fonte. A ausência é preservada,
# em vez de ser preenchida com um valor estimado sem respaldo.
indicadores = [
    'populacao_2024', 'populacao_2025', 'idhm_2010',
    'pib_per_capita_2023_reais',
    'densidade_hab_km2', 'area_km2',
]
indicadores_ausentes = dim_municipio[indicadores].isna().sum()
for indicador, quantidade in indicadores_ausentes.items():
    if quantidade:
        for _, row in dim_municipio[dim_municipio[indicador].isna()].iterrows():
            inconsistencias.append({
                'severidade': 'AVISO',
                'tipo': 'indicador_ausente',
                'municipio': row['município'],
                'detalhe': f'{indicador} ausente na fonte municipios-brasil.csv',
            })

df_inc = pd.DataFrame(
    inconsistencias,
    columns=['severidade', 'tipo', 'municipio', 'detalhe'],
)
df_inc.to_csv(os.path.join(processed_dir, 'inconsistencias.csv'), index=False)
print(f"Inconsistências documentadas: {len(df_inc)}")
print(f"Salvo em: {os.path.join(processed_dir, 'inconsistencias.csv')}")

# =========================================================================
# 9. RELATÓRIO DE VALIDAÇÃO
# =========================================================================

print("\n--- RELATÓRIO DE VALIDAÇÃO ---")
chaves_dim = set(dim_municipio['chave_municipal'].dropna())
chaves_fato = set(fato_repasses['chave_municipal'].dropna())
chaves_orfas = len(chaves_fato - chaves_dim)
codigos_ibge_duplicados = int(dim_municipio['codigo_ibge'].duplicated().sum())

validacoes = []


def registra_validacao(metrica, valor, esperado, aprovada, critica=True):
    validacoes.append({
        'metrica': metrica,
        'valor': valor,
        'esperado': esperado,
        'status': 'OK' if aprovada else ('ERRO' if critica else 'AVISO'),
    })


registra_validacao(
    'total_registros_fato', len(fato_repasses), EXPECTED_TOTAL_REGISTROS,
    len(fato_repasses) == EXPECTED_TOTAL_REGISTROS,
)
registra_validacao(
    'total_municipios_dim', len(dim_municipio), EXPECTED_TOTAL_MUNICIPIOS,
    len(dim_municipio) == EXPECTED_TOTAL_MUNICIPIOS,
)
registra_validacao(
    'negativos_preservados', len(valores_negativos), EXPECTED_NEGATIVOS,
    len(valores_negativos) == EXPECTED_NEGATIVOS,
)
registra_validacao(
    'soma_total_fato', round(total_fato, 2), EXPECTED_TOTAL_FATO,
    abs(total_fato - EXPECTED_TOTAL_FATO) <= TOLERANCIA_MONETARIA,
)
registra_validacao(
    'soma_total_ranking', round(total_ranking, 2), EXPECTED_TOTAL_RANKING,
    abs(total_ranking - EXPECTED_TOTAL_RANKING) <= TOLERANCIA_MONETARIA,
)
registra_validacao(
    'diferenca_conciliacao', round(diferenca, 2), EXPECTED_DIFERENCA,
    abs(diferenca - EXPECTED_DIFERENCA) <= TOLERANCIA_MONETARIA,
)
registra_validacao(
    'municipios_sem_ibge', int(dim_municipio['codigo_ibge'].isna().sum()), 0,
    dim_municipio['codigo_ibge'].notna().all(),
)
registra_validacao(
    'codigos_ibge_duplicados', codigos_ibge_duplicados, 0,
    codigos_ibge_duplicados == 0,
)
registra_validacao(
    'municipios_rs_populacao_sidra_2024', len(df_populacao_rs_2024),
    EXPECTED_MUNICIPIOS_RS,
    len(df_populacao_rs_2024) == EXPECTED_MUNICIPIOS_RS,
)
registra_validacao(
    'municipios_receptores_sem_populacao_2024', len(sem_populacao_2024), 0,
    sem_populacao_2024.empty,
)
registra_validacao(
    'localizacoes_mapa_duplicadas', localizacoes_duplicadas, 0,
    localizacoes_duplicadas == 0,
)
registra_validacao(
    'fato_sem_chave_municipal', int(fato_repasses['chave_municipal'].isna().sum()), 0,
    fato_repasses['chave_municipal'].notna().all(),
)
registra_validacao(
    'chaves_municipais_orfas', chaves_orfas, 0, chaves_orfas == 0,
)
registra_validacao(
    'duplicatas_exatas', int(duplicadas), 0, duplicadas == 0,
)
registra_validacao(
    'datas_invalidas', datas_invalidas, 0, datas_invalidas == 0,
)
registra_validacao(
    'valores_nulos', len(nulos_valor), 0, len(nulos_valor) == 0,
)
registra_validacao(
    'movimentacoes_sem_municipio', len(municipios_ausentes_origem), 0,
    len(municipios_ausentes_origem) == 0,
)
registra_validacao(
    'indicadores_ausentes', int(indicadores_ausentes.sum()), 0,
    indicadores_ausentes.sum() == 0,
    critica=False,
)
registra_validacao(
    'total_intervalos_municipais', len(intervalo_primeiro_repasse),
    EXPECTED_INTERVALOS,
    len(intervalo_primeiro_repasse) == EXPECTED_INTERVALOS,
)
status_intervalos_invalidos = int(
    intervalo_primeiro_repasse['status_intervalo'].ne('ok').sum()
)
registra_validacao(
    'intervalos_sem_status_ok', status_intervalos_invalidos, 0,
    status_intervalos_invalidos == 0,
)
registra_validacao(
    'estornos_ignorados_no_primeiro_repasse',
    int(intervalo_primeiro_repasse['qtd_estornos_ignorados'].sum()),
    EXPECTED_NEGATIVOS,
    int(intervalo_primeiro_repasse['qtd_estornos_ignorados'].sum())
    == EXPECTED_NEGATIVOS,
)

df_validacao = pd.DataFrame(validacoes)
df_validacao.to_csv(os.path.join(processed_dir, 'relatorio_validacao.csv'), index=False)

for _, row in df_validacao.iterrows():
    print(f"  [{row['status']}] {row['metrica']}: {row['valor']} (esperado: {row['esperado']})")

print(f"\nRelatório de validação salvo em: {os.path.join(processed_dir, 'relatorio_validacao.csv')}")

falhas_criticas = df_validacao[df_validacao['status'] == 'ERRO']
if not falhas_criticas.empty:
    metricas = ', '.join(falhas_criticas['metrica'])
    raise RuntimeError(f'Validação do ETL falhou: {metricas}')

# =========================================================================
# 10. EXPORTAÇÃO SQLITE
# =========================================================================

exportar_sqlite(
    df_ranking,
    dim_municipio,
    fato_repasses,
    dim_calendario,
    intervalo_primeiro_repasse,
)

print(f"\nCSVs prontos para o Qlik Sense em: {processed_dir}")
print(f"  - fato_repasses.csv (com chave_municipal)")
print(f"  - dim_municipio.csv (com indicadores IBGE, IDH-M, PIB)")
print(f"  - dim_calendario.csv")
print(f"  - intervalo_primeiro_repasse.csv")
print(f"  - conciliacao.csv")
print(f"  - inconsistencias.csv")
print(f"  - relatorio_validacao.csv")
print(f"\nBanco SQLite atualizado em: {db_path}")
