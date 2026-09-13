# Task 10 — Intervalo até o primeiro repasse elegível

## Definição adotada

A métrica calcula, por município, o número de dias entre **24/04/2024** e
a primeira movimentação positiva registrada na base detalhada do FUNDEC/RS.

- **Marco adotado:** início do período estadual dos eventos climáticos.
- **Fonte do marco:** art. 1º do Decreto Estadual RS nº 57.604, de
  7 de maio de 2024, disponível em
  [`data/raw/pdf/Decreto-57604-2024-Rio-grande-do-sul-RS.pdf`](../data/raw/pdf/Decreto-57604-2024-Rio-grande-do-sul-RS.pdf).
- **Universo municipal:** os 334 municípios com repasses na base detalhada e
  no ranking do FUNDEC/RS.
- **Primeiro repasse elegível:** menor data de uma movimentação com
  `valor > 0` e data válida.
- **Nome da medida:** `intervalo_desde_marco_adotado_dias`.

O marco é comum aos municípios porque o decreto caracteriza o período do
evento estadual que fundamenta o regime excepcional desses repasses. Ele não
é interpretado como a data em que cada município sofreu seu primeiro impacto.

## Tratamento de qualidade

O cálculo preserva todas as movimentações na tabela fato, inclusive os 18
estornos. Valores negativos não iniciam atendimento. A saída usa os seguintes
estados:

| Status | Tratamento |
|---|---|
| `ok` | Publica o intervalo inteiro em dias. |
| `sem_data_marco` | Mantém o intervalo nulo. |
| `sem_primeiro_repasse_elegivel` | Mantém o intervalo nulo. |
| `intervalo_negativo` | Sinaliza a inconsistência e mantém o intervalo nulo. |

Marcos municipais duplicados interrompem o cálculo com erro, evitando uma
relação muitos-para-muitos acidental.

## Resultado

- 334 municípios calculados;
- 334 registros com status `ok`;
- primeira data elegível entre 17/05/2024 e 06/09/2024;
- intervalo entre 23 e 135 dias;
- mediana de 28 dias e média de 40,13 dias;
- 18 estornos ignorados somente na escolha da primeira data.

## Conferência manual da amostra

As movimentações dos municípios abaixo foram conferidas diretamente em
`fato_repasses.csv`. A diferença foi recalculada a partir de 24/04/2024.

| Município | Primeiro crédito | Intervalo (dias) | Estornos ignorados |
|---|---:|---:|---:|
| Canoas | 20/06/2024 | 57 | 0 |
| Ivorá | 10/07/2024 | 77 | 0 |
| Porto Alegre | 17/07/2024 | 84 | 1 |
| Pirapó | 26/07/2024 | 93 | 2 |
| Charqueadas | 06/09/2024 | 135 | 0 |

Pirapó confirma o caso de borda principal: os estornos de 29/07 e 02/08 não
alteram o primeiro crédito elegível de 26/07. Porto Alegre também preserva o
crédito de 17/07 como primeiro repasse, apesar do estorno posterior de 18/07.

## Artefatos

- cálculo reutilizável: `etl/metricas_repasses.py`;
- integração no pipeline: `etl/analis_de_dados.py`;
- saída municipal: `data/processed/intervalo_primeiro_repasse.csv`;
- tabela SQLite: `intervalo_primeiro_repasse`;
- carga no Qlik: `qlik/load_data.qvs`;
- testes de regra e qualidade: `tests/test_metricas_repasses.py` e
  `tests/test_etl_outputs.py`.

## Limites de interpretação

Esta métrica não mede o tempo desde o impacto local, a solicitação municipal,
a habilitação, o deferimento ou a ordem bancária. Essas datas não estão na
base atual. O intervalo combina um marco documental estadual comum com a data
registrada da primeira movimentação positiva e não permite atribuir causa ao
prazo observado.
