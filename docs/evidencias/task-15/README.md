# Evidências da Task 15 — Tela 2 (Linha do Tempo)

**Estado:** três capturas do Qlik Cloud adicionadas e valores mensais do app conferidos com a base processada.

## Capturas

| Arquivo | O que deve aparecer |
|---|---|
| [`01-tela2-evolucao-mensal.png`](01-tela2-evolucao-mensal.png) | Tela 2 em modo de visualização, sem filtros; título, eixo de 202405 a 202409 em ordem cronológica, legenda e séries de créditos, ajustes negativos e saldo líquido. |
| [`02-tela2-filtro.png`](02-tela2-filtro.png) | Seleção de julho de 2024 no campo `ano_mes_ordem`; o gráfico passa a exibir apenas 202407. |
| [`03-tela2-dados-mensais.png`](03-tela2-dados-mensais.png) | Visão de dados do mesmo gráfico, sem seleção, com os cinco meses e os valores completos das três medidas. |

**Seleção usada no segundo print:** `ano_mes_ordem = 202407` (julho de 2024).

As capturas mostram a ordem dos meses, as três medidas e o efeito da seleção. A caixa de seleção aberta no segundo print cobre parte do título e do gráfico; o primeiro print registra a visualização completa. O terceiro print mostra os valores completos do Qlik, que não são legíveis nos eixos abreviados do gráfico.

## Valores de referência

Calculados a partir de `data/processed/fato_repasses.csv`, agrupando as movimentações por mês da coluna `data`. Créditos são valores positivos; ajustes são valores negativos; saldo líquido é a soma dos dois.

| Mês | Créditos | Ajustes negativos | Saldo líquido |
|---|---:|---:|---:|
| 2024-05 | R$ 47.000.000,00 | −R$ 4.800.000,00 | R$ 42.200.000,00 |
| 2024-06 | R$ 166.625.581,37 | −R$ 1.869.767,44 | R$ 164.755.813,93 |
| 2024-07 | R$ 80.289.534,88 | −R$ 11.565.116,28 | R$ 68.724.418,60 |
| 2024-08 | R$ 6.617.441,86 | −R$ 400.000,00 | R$ 6.217.441,86 |
| 2024-09 | R$ 6.802.325,58 | R$ 0,00 | R$ 6.802.325,58 |
| **Total** | **R$ 307.334.883,69** | **−R$ 18.634.883,72** | **R$ 288.699.999,97** |

As cinco linhas da visão de dados do Qlik foram comparadas com esta tabela. Créditos, ajustes negativos e saldo líquido coincidem em todos os meses. A soma das linhas confirma os três totais; a visão de dados não exibe uma linha de total. Na interface do Qlik, os números aparecem sem separador de milhar e com ponto decimal.

## Conferência após incluir as imagens

- [x] Os três arquivos PNG foram adicionados a esta pasta e abrem normalmente.
- [x] A ordem do eixo e as três medidas são legíveis no primeiro print.
- [x] A seleção e o efeito sobre os valores são legíveis no segundo print, em conjunto com o primeiro.
- [x] As cinco linhas exibidas pelo app foram confrontadas com os valores de referência; os totais foram obtidos pela soma dessas linhas.
- [x] O README do snapshot 06 foi atualizado com o resultado da conferência visual.
