# Task 17 — Tela 4: concentração dos repasses FUNDEC (H5)

## Universo e regra de cálculo

A análise usa as 658 movimentações detalhadas em
[`data/processed/fato_repasses.csv`](../data/processed/fato_repasses.csv), de maio a
setembro de 2024. Há 334 municípios com movimentação no período. O valor
líquido de cada município é `Sum(valor)`: créditos positivos e ajustes
negativos permanecem com seus sinais. O total líquido desse universo é
**R$ 288.699.999,97**. A análise não usa `valor_pago` como denominador, pois o
ranking oficial possui uma diferença de R$ 476.004,28 em relação às
movimentações detalhadas, documentada na
[Task 12](./task-12-calculos-reutilizaveis.md#conciliação).

Os municípios são ordenados pelo valor líquido em ordem decrescente. Em cada
corte, a participação é a soma dos valores dos primeiros municípios dividida
pelo total líquido dos 334. A seleção dos 20 maiores foi salva como marcador
no Qlik. Esse marcador guarda os municípios selecionados; o ranking deve ser
reconferido após uma atualização dos dados.

| Corte por valor líquido | Valor líquido | Participação no total |
|---|---:|---:|
| 5 maiores | R$ 28.912.790,70 | 10,01% |
| 10 maiores | R$ 55.729.069,78 | 19,30% |
| 20 maiores | R$ 98.238.372,09 | 34,03% |

Os 20 maiores são **20 de 334 municípios (5,99%)**. Na tabela da Tela 4, a
participação municipal tem como expressão de referência
`Sum(valor) / Sum({1} TOTAL valor)`. O conjunto `{1}`
mantém como denominador a base completa mesmo com o marcador dos 20 ativo.
Assim, esse indicador compara a seleção atual com o total do período inteiro;
filtros adicionais no numerador não alteram o denominador.

## Créditos e ajustes negativos

Os créditos dos 334 municípios somam R$ 307.334.883,69. Os 18 lançamentos
negativos somam **−R$ 18.634.883,72**, resultando no total líquido acima. Para
o grupo dos 20 maiores por valor líquido:

| Componente | Total do grupo |
|---|---:|
| Créditos recebidos | R$ 110.603.488,37 |
| Ajustes negativos | −R$ 12.365.116,28 |
| Valor líquido recebido | R$ 98.238.372,09 |

O grupo representa 35,99% dos créditos de todos os municípios e 34,03% do
valor líquido. Os ajustes diminuem a participação do grupo no total líquido e
afetam a ordem interna. Porto Alegre ilustra o efeito: R$ 16.247.674,42 em
créditos, −R$ 10.465.116,28 em ajustes e R$ 5.782.558,14 líquidos. Na base
atual, os integrantes dos 20 maiores por créditos e por valor líquido são os
mesmos; sua ordem pode mudar.

## Comparação por pessoa e interpretação

O valor por pessoa divide o valor líquido municipal pela população estimada
para 2024 em `dim_municipio.csv`, usando uma única população por município.
Essa divisão é válida para comparar escala populacional entre municípios, mas
**não representa o repasse por pessoa atingida**, pois a população total não é
uma contagem de pessoas afetadas. A medida reutilizável e suas regras estão em
[`qlik/medidas-mestras.md`](../qlik/medidas-mestras.md#5-valor-líquido-por-pessoa).

A Tela 4 permite comparar o valor por pessoa dentro do grupo de 20 maiores por
valor líquido. Sem o marcador, o mesmo gráfico mostra o ranking por pessoa da
base completa. Os primeiros 20 desse ranking são diferentes dos 20 maiores por
valor absoluto; não há município em comum entre os dois grupos na base
versionada. Isso mostra por que os dois critérios precisam de rótulos e
interpretações separados.

O corte de 20 municípios indica concentração em relação à proporção de
municípios atendidos: 5,99% deles receberam 34,03% do valor líquido. Ele **não
confirma** que esse grupo recebeu a maioria dos recursos, caso “maioria”
signifique mais de 50%. A conclusão se limita a este universo, período e
definição de saldo líquido. Não permite inferir se os repasses foram
proporcionais aos danos ou às necessidades locais.

## Evidências e versão do aplicativo

As cinco capturas, os recortes aplicados e o que cada imagem comprova estão em
[`docs/evidencias/task-17/README.md`](./evidencias/task-17/README.md). O
snapshot exportado do Qlik está em
[`qlik/versoes-do-app/08-task-17/`](../qlik/versoes-do-app/08-task-17/README.md).

Os totais exatos desta página foram recalculados a partir dos CSVs processados.
O KPI do print mostra **98,24M** e **34%** por arredondamento visual; a captura
da tabela mostra as linhas municipais com valores monetários completos.
