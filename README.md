# SQLite + Qlik Sense — Integração FUNDEC/RS

Tutorial de integração do banco SQLite com o Qlik Sense para visualização dos dados de repasses do **FUNDEC** (Fundo de Defesa Civil do Estado do Rio Grande do Sul) — enchentes de 2024.

---

## O que é este projeto

O FUNDEC é o fundo estadual que transfere recursos para municípios do RS em situação de emergência ou calamidade pública. Após as enchentes de 2024, centenas de municípios receberam repasses para reconstrução.

Este projeto coleta dados públicos sobre esses repasses e armazena em um banco SQLite para análise e visualização no Qlik Sense.

### Fontes de dados

| Arquivo | O que contém | Tabela no banco |
|---------|-------------|-----------------|
| `ranking_oficial_fundec_2024.csv` | Ranking dos municípios por valor total recebido | `dim_ranking` |
| `repasses_fundec_2024.csv` | Detalhes de cada transferência individual | `fato_repasses` |

> Os PDFs na pasta `data/raw/pdf/` são documentos legais (decretos, leis). Servem como referência, não são dados para o banco.

---

## Banco de Dados

Arquivo: `database/banco_hackathon.db`

### `dim_ranking` — Ranking por município (334 registros)

Cada linha é um município com o total de recursos recebidos.

| Coluna | Tipo | Exemplo |
|--------|------|---------|
| município | TEXT | Canoas |
| valor_pago_(r$) | TEXT | 5958562,42 |

### `fato_repasses` — Transferências individuais (658 registros)

Cada linha é um repasse do FUNDEC para um município.

| Coluna | Tipo | Exemplo |
|--------|------|---------|
| data | TIMESTAMP | 2024-09-26 00:00:00 |
| processo | INTEGER | 24080400010231 |
| recurso | TEXT | Judiciário |
| empenho | INTEGER | 24005579303 |
| cnpj | INTEGER | 55397324000105 |
| credor | TEXT | Fundo Mun Defesa Civil de Ivora |
| município | TEXT | Ivora |
| valor | REAL | 784883.72 |

---

## Como rodar

### 1. Instalar dependência

```bash
pip install pandas
```

### 2. Rodar o ETL

O script `etl/analis_de_dados.py` lê os CSVs e salva no banco SQLite:

```bash
python etl/analis_de_dados.py
```

### 3. Verificar se funcionou

```bash
# Ver schema das tabelas
sqlite3 database/banco_hackathon.db ".schema"

# Contar registros
sqlite3 database/banco_hackathon.db "SELECT COUNT(*) FROM dim_ranking;"
sqlite3 database/banco_hackathon.db "SELECT COUNT(*) FROM fato_repasses;"
```

Deve retornar **334** para dim_ranking e **658** para fato_repasses.

---

## Conectar no Qlik Sense

### Pré-requisito: Driver ODBC

O Qlik Sense se comunica com o SQLite via driver ODBC. Instale em:
https://www.ch-werner.de/sqliteodbd/

### Script de carga

No **Data Load Editor** do Qlix Sense, copie e cole:

```qlik
// Caminho do banco SQLite (ajuste para o seu computador)
LIB SQL [/home/usuario/Hackaton-Excelsior-/database/banco_hackathon.db];

// Ranking dos municípios
dim_ranking:
LOAD
    *,
    RowNo() AS id_ranking;
SQL
SELECT "munic\u00EDpio" AS municipio, "valor_pago_(r$)" AS valor_pago
FROM dim_ranking;

// Detalhes dos repasses
fato_repasses:
LOAD
    *,
    RowNo() AS id_repasses;
SQL
SELECT data, processo, recurso, empenho, cnpj, credor,
       "munic\u00EDpio" AS municipio, valor
FROM fato_repasses;
```

> **Importante:** Substitua o caminho no `LIB SQL` pelo caminho real do `banco_hackathon.db` no seu computador.

### Após carregar

1. Clique em **Carregar dados**
2. Se aparecer "Carga concluída com sucesso", está tudo certo
3. Vá para **Visão de dados** para criar gráficos e tabelas

---

## Referência SQL — Top 5 comandos

### Ver todos os dados

```sql
SELECT * FROM fato_repasses;
```

### Filtrar por município

```sql
SELECT * FROM fato_repasses WHERE município = 'Porto Alegre';
```

### Top 10 municípios que mais receberam

```sql
SELECT município, SUM(valor) as total
FROM fato_repasses
GROUP BY município
ORDER BY total DESC
LIMIT 10;
```

### Contar repasses por município

```sql
SELECT município, COUNT(*) as quantidade
FROM fato_repasses
GROUP BY município
ORDER BY quantidade DESC;
```

### Valor total por tipo de recurso

```sql
SELECT recurso, SUM(valor) as total, COUNT(*) as qtd
FROM fato_repasses
GROUP BY recurso;
```

---

## Troubleshooting

| Erro | Causa | Solução |
|------|-------|---------|
| `No such file` | Caminho dos CSVs errado | Executar ETL da raiz do projeto |
| Tabela não encontrada | Banco não gerado | Rodar `python etl/analis_de_dados.py` |
| Coluna não encontrada | Nome com acento | Usar `"munic\u00EDpio"` no script Qlik |
| Conexão recusada | Driver ODBC ausente | Instalar driver SQLite ODBC |
| Encoding estranho | BOM no CSV | ETL já usa `utf-8-sig` |
| Valor zero no gráfico | Tipo errado | Verificar se `valor` é REAL no schema |
