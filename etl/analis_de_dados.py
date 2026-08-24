import pandas as pd
import sqlite3

df = pd.read_excel('/home/segfaults433y/dev/estudos/Hackthon/data (2).xlsx')
df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()

print(df.shape)
print(df.columns)
print(df.head())
print(df.dtypes)
print(df.isna().sum())

print("\nVALORES NULOS")
print(df[df.isna().any(axis=1)])

print("\nVALORES")
print(df["valor"].describe())

print("\nVALORES NEGATIVOS")
print(df[df["valor"] < 0])

print("\nMUNICÍPIOS")
print(df["município"].value_counts())

print("\nRECURSOS")
print(df["recurso"].value_counts(dropna=False))

# limpeza dos totais e nan do powerbi
df_limpo = df.dropna(subset=['município']).copy()

# formataçao de tipos
df_limpo['data'] = pd.to_datetime(df_limpo['data'], errors='coerce')

colunas_ids = ['processo', 'empenho', 'cnpj']
for col in colunas_ids:
    df_limpo[col] = df_limpo[col].astype('Int64').astype(str).replace('<NA>', '')

# salvando no banco local pro qlik consumir
db_path = '/home/segfaults433y/dev/estudos/Hackthon/banco_hackathon.db'
conn = sqlite3.connect(db_path)
df_limpo.to_sql('fato_repasses', conn, if_exists='replace', index=False)
conn.close()