# SQLite + Qlik Sense — Integração FUNDEC/RS

Análise da distribuição de recursos do **FUNDEC** (Fundo de Defesa Civil do Estado do Rio Grande do Sul) para municípios atingidos pelas enchentes de 2024. Pipeline ETL + banco analítico + dashboard Qlik Sense.

## Documentação do Hackathon

- [Orientações atualizadas de submissão (prazo 23/09/2026)](docs/atualizacao-submissao-2026-09-18.md)
- [Edital explicado e especificação do projeto](docs/edital-hackathon-qlik-2026.md)
- [Requisitos e status do projeto](docs/requisitos-e-status.md)
- [Relatório descritivo final](docs/relatorio-final.md)

---

## O que é este projeto

O FUNDEC transfere recursos para municípios do RS em situação de emergência ou calamidade pública. Após as enchentes de 2024, centenas de municípios receberam repasses para reconstrução.

Este projeto coleta dados públicos sobre esses repasses, aplica um pipeline de limpeza e validação, e gera um banco analítico estrela (star schema) para visualização no Qlik Sense.

### Fontes de dados

| Arquivo | O que contém | Uso no ETL |
|---------|-------------|------------|
| `repasses_fundec_2024.csv` | 658 transferências individuais do FUNDEC | Tabela fato (`fato_repasses`) |
| `ranking_oficial_fundec_2024.csv` | Ranking dos 334 municípios por valor total | Referência para conciliação |
| `municipios-brasil.csv` | 5.571 municípios brasileiros com código IBGE, IDH-M, PIB, densidade | Dimensão municipal (`dim_municipio`) |
| `populacao_rs_2024.csv` | População estimada dos 497 municípios do RS (SIDRA T6579) | Denominador municipal dos repasses por pessoa |
| `defesa-civil-rs-municipios-afetados-2024-06-11.pdf` | Extrato oficial com 478 municípios afetados em 11/06/2024 | Comparação de cobertura da Task 16; não define elegibilidade ao FUNDEC |

> Os PDFs em `data/raw/pdf/` são documentos legais de referência, não são dados para o banco.

---

## Modelo de dados (Star Schema)

### `fato_repasses` — Transferências individuais (658 registros)

Cada linha é um repasse do FUNDEC para um município. Inclui 18 estornos (valores negativos).

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `data` | DATE | Data do repasse (YYYY-MM-DD) |
| `chave_municipal` | TEXT | Chave municipal IBGE (7 dígitos, FK para `dim_municipio`) |
| `processo` | TEXT | Número do processo administrativo |
| `empenho` | TEXT | Nota de empenho |
| `cnpj` | TEXT | CNPJ do fundo municipal |
| `credor` | TEXT | Nome do fundo credor |
| `recurso` | TEXT | Tipo do recurso (Judiciário ou Tesouro) |
| `valor` | REAL | Valor do repasse com sinal (negativo = estorno) |

### `dim_municipio` — Dimensão municipal (334 registros)

Todos os municípios do ranking com código IBGE e indicadores socioeconômicos.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `chave_municipal` | TEXT | Chave municipal IBGE (PK, 7 dígitos) |
| `município` | TEXT | Nome do município |
| `codigo_ibge` | INT | Código IBGE (7 dígitos) |
| `municipio_ibge_2024` | TEXT | Nome oficial usado na fonte populacional do IBGE |
| `localizacao_mapa` | TEXT | Município, estado e país para geocodificação no Qlik |
| `regiao` | TEXT | Região (Sul) |
| `populacao_2024` | INT | População municipal estimada pelo IBGE/SIDRA em 2024 |
| `populacao_2025` | INT | População estimada 2025 |
| `populacao_censo_2022` | FLOAT | População Censo 2022 |
| `idhm_2010` | FLOAT | IDHM 2010 (0 a 1) |
| `pib_per_capita_2023_reais` | FLOAT | PIB per capita 2023 (R$) |
| `pib_2023_mil_reais` | FLOAT | PIB 2023 (mil R$) |
| `densidade_hab_km2` | FLOAT | Densidade demográfica |
| `area_km2` | FLOAT | Área territorial (km²) |
| `valor_pago` | FLOAT | Total pago conforme ranking oficial |
| `total_repasses` | FLOAT | Soma dos repasses na fato |
| `valor_por_pessoa_2024` | FLOAT | Total líquido dividido pela população estimada de 2024 |
| `qtd_repasses` | INT | Quantidade de repasses |
| `valor_medio` | FLOAT | Valor médio por repasse |

### `dim_calendario` — Dimensão tempo (133 registros)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `data` | DATE | Data diária entre 17/05/2024 e 26/09/2024 |
| `ano` | INT | Ano |
| `trimestre` | TEXT | Trimestre no formato T1–T4 |
| `mes` | INT | Número do mês |
| `mes_nome` | TEXT | Nome do mês em português |
| `ano_mes` | TEXT | Ano e mês no formato YYYY-MM |
| `ano_mes_ordem` | INT | Campo numérico para ordenação cronológica |

### `dim_ranking` — Ranking oficial (334 registros)

Tabela original do ranking, mantida como referência.

### `intervalo_primeiro_repasse` — Intervalo municipal (334 registros)

Calcula a menor data com `valor > 0` para cada município. O marco adotado é
24/04/2024, início do período estadual dos eventos documentado pelo Decreto
Estadual RS nº 57.604/2024. A medida se chama
`intervalo_desde_marco_adotado_dias`: ela não representa necessariamente o
tempo desde o impacto local e não atribui causa ao prazo.

---

## Arquivos gerados

Após executar o ETL, os seguintes arquivos são salvos em `data/processed/`:

| Arquivo | Uso |
|---------|-----|
| `fato_repasses.csv` | Tabela fato para carga no Qlik |
| `dim_municipio.csv` | Dimensão municipal para carga no Qlik |
| `dim_calendario.csv` | Dimensão tempo para carga no Qlik |
| `intervalo_primeiro_repasse.csv` | Marco documentado, primeiro crédito positivo e intervalo por município |
| `conciliacao.csv` | Comparativo fato vs ranking por município |
| `relatorio_validacao.csv` | Métricas de validação do pipeline |
| `inconsistencias.csv` | Erros e ausências conhecidas nas fontes |
| `doc_18_valores_negativos.csv` | Documentação dos 18 estornos |
| `municipios_afetados_defesa_civil_2024_06_11.csv` | Lista da Defesa Civil associada aos códigos IBGE |
| `cobertura_municipal.csv` | 497 municípios do RS com presença na lista e situação na base FUNDEC |
| `casos_cobertura_investigacao.csv` | Casos para revisar, sem inferir ausência de atendimento |
| `relatorio_cobertura.csv` | Contagens e períodos do cruzamento de cobertura |

O banco SQLite `banco_hackathon.db` também é gerado na raiz do projeto.

---

## Como rodar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o ETL

```bash
python etl/analis_de_dados.py
python etl/cobertura_municipal.py
python etl/analise_idhm_repasses.py
```

### 3. Validar a saída

O ETL imprime métricas de validação e termina com erro caso um critério
crítico não seja atendido. Resultados esperados:

```
Registros negativos preservados: 18
Todos os 334 municípios associados ao IBGE.
Total Detalhado (Fato): R$ 288,699,999.97
Total Oficial (Ranking): R$ 289,176,004.25
Diferença: R$ -476,004.28
```

Verificar o relatório detalhado:

```bash
cat data/processed/relatorio_validacao.csv
```

Executar também os testes dos artefatos e do esquema SQLite:

```bash
python -m unittest discover -s tests -v
```

---

## Conectar no Qlik Sense

### Opção 1: Carregar via CSV (recomendado)

O método recomendado utiliza os CSVs processados via conexão `DataFiles` e **não requer driver ODBC**.

### Opção 2: Carregar via SQLite (alternativa)

Caso prefira carregar direto do SQLite, o Qlik Sense se comunica via driver ODBC. Instale em:
https://www.ch-werner.de/sqliteodbd/

Envie os CSVs de `data/processed/` para a conexão `DataFiles` e execute o script no **Data Load Editor** do Qlik Sense:

```qlik
// Dimensão municipal
dim_municipio:
LOAD *
FROM [lib://DataFiles/dim_municipio.csv]
(utf8, txt, embedded labels, delimiter is ',', msq);

// Fato de repasses
fato_repasses:
LOAD *
FROM [lib://DataFiles/fato_repasses.csv]
(utf8, txt, embedded labels, delimiter is ',', msq);

// Dimensão calendário
dim_calendario:
LOAD *
FROM [lib://DataFiles/dim_calendario.csv]
(utf8, txt, embedded labels, delimiter is ',', msq);
```

O script completo está em `qlik/load_data.qvs` e inclui também
`intervalo_primeiro_repasse.csv` e `cobertura_municipal.csv` (Task 16).
Envie os cinco CSVs à conexão e substitua `DataFiles` pelo nome configurado
no seu ambiente. A tabela de cobertura foi carregada e conferida no Qlik no
snapshot 09. Adicione o arquivo à conexão sem carregá-lo outra vez pelo
Gerenciador de dados: duas cargas do mesmo CSV criam campos duplicados e uma
chave sintética.

### Opção 2: Carregar via SQLite

```qlik
LIB CONNECT TO 'SQLite_FUNDEC';

dim_municipio:
LOAD *;
SQL SELECT * FROM dim_municipio;

fato_repasses:
LOAD *;
SQL SELECT * FROM fato_repasses;

dim_calendario:
LOAD *;
SQL SELECT * FROM dim_calendario;
```

> **Importante:** Ajuste os caminhos conforme seu ambiente.

### Versionamento do app Qlik

Os snapshots do app ficam em `qlik/versoes-do-app/`. Ao baixar um app do
Qlik para criar uma nova versão, selecione obrigatoriamente a opção **com
dados**. Assim, o arquivo QVF preserva os dados carregados e pode ser
visualizado após a importação sem exigir uma recarga imediata.

Consulte `qlik/versoes-do-app/README.md` para a convenção de nomes e o processo
de inclusão de novas versões.

### Limitação conhecida dos indicadores

`Pinto Bandeira` não possui `idhm_2010` na fonte `municipios-brasil.csv`.
O valor permanece nulo, sem imputação, e a ausência é registrada em
`data/processed/inconsistencias.csv`.

### Modelo de associação no Qlik

```
dim_municipio (chave_municipal) ←→ fato_repasses (chave_municipal)
dim_calendario (data) ←→ fato_repasses (data)
dim_municipio (chave_municipal) ←→ intervalo_primeiro_repasse (chave_municipal)
cobertura_municipal (chave_municipal) ←→ dim_municipio (chave_municipal)
```

O modelo atual do app não possui chaves sintéticas. A associação da nova tabela
de cobertura deve ser reconferida após a recarga no Qlik; `chave_municipal` é
o único campo compartilhado com as tabelas já carregadas.

---

## Referência SQL

### Ver todos os repasses

```sql
SELECT * FROM fato_repasses;
```

### Top 10 municípios que mais receberam

```sql
SELECT d."município", SUM(f.valor) as total
FROM fato_repasses f
JOIN dim_municipio d ON f.chave_municipal = d.chave_municipal
GROUP BY d."município"
ORDER BY total DESC
LIMIT 10;
```

### Repasses com indicadores socioeconômicos

```sql
SELECT d."município", d.idhm_2010, d.pib_per_capita_2023_reais,
       d.densidade_hab_km2, SUM(f.valor) as total
FROM fato_repasses f
JOIN dim_municipio d ON f.chave_municipal = d.chave_municipal
GROUP BY d."município"
ORDER BY total DESC;
```

### Valor total por tipo de recurso

```sql
SELECT recurso, SUM(valor) as total, COUNT(*) as qtd
FROM fato_repasses
GROUP BY recurso;
```

### Municípios com estornos (valores negativos)

```sql
SELECT d."município", f.valor, f.data
FROM fato_repasses f
JOIN dim_municipio d ON f.chave_municipal = d.chave_municipal
WHERE f.valor < 0
ORDER BY f.valor;
```

---

## Equipe

Este projeto foi desenvolvido por 3 integrantes:

- **Sallys Moraes Martins** — Desenvolvimento do pipeline ETL (Python/Pandas), modelagem de dados, validações automatizadas, integração Qlik Sense, documentação técnica
- [Nome do 2º integrante] — [Função/Contribuição]
- [Nome do 3º integrante] — [Função/Contribuição]

> *Preencher os demais integrantes antes da entrega final.*

---

## Troubleshooting

| Erro | Causa | Solução |
|------|-------|---------|
| `No such file` | Caminho dos CSVs errado | Executar ETL da raiz do projeto |
| Tabela não encontrada | Banco não gerado | Rodar `python etl/analis_de_dados.py` |
| Coluna não encontrada | Nome com acento | Usar `"munic\u00EDpio"` no script Qlik |
| Conexão recusada | Driver ODBC ausente | Instalar driver SQLite ODBC |
| 0 registros no Qlik | Encoding errado | CSVs usam UTF-8 sem BOM |
| Valores zerados | Tipo errado | Verificar se `valor` é REAL no schema |
