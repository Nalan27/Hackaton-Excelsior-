# Evidências da Task 17 — Tela 4 (Concentração — H5)

As capturas foram feitas no Qlik Cloud em 16/09/2026. O marcador seleciona os
20 maiores municípios pelo valor líquido das movimentações detalhadas. A
[análise e os totais exatos](../../task-17-concentracao.md) documentam a regra
de cálculo e a interpretação.

| Arquivo | Seleção visível | Evidência |
|---|---|---|
| [`01-top20-saldo-liquido.png`](01-top20-saldo-liquido.png) | 20 de 334 municípios | Os 20 municípios selecionados e seus saldos líquidos em ordem decrescente. |
| [`02-participacao-e-ajustes.png`](02-participacao-e-ajustes.png) | 20 de 334 municípios | Tabela com líquido, créditos, ajustes, participação no total da base e R$ por pessoa; Porto Alegre mostra o efeito do ajuste negativo. |
| [`03-per-capita-nos-top20-liquido.png`](03-per-capita-nos-top20-liquido.png) | 20 de 334 municípios | Ordenação por R$ por pessoa **dentro do grupo selecionado por saldo líquido**. |
| [`04-per-capita-base-completa.png`](04-per-capita-base-completa.png) | Nenhuma seleção | Ranking por R$ por pessoa na base completa, com os maiores valores nas primeiras barras e mais municípios acessíveis pela rolagem. |
| [`05-tela4-kpi.png`](05-tela4-kpi.png) | 20 de 334 municípios | Vista da pasta com gráfico, tabela e KPI: 98,24M e 34% na formatação abreviada do Qlik. |

## Conferência

- Os 20 municípios do primeiro gráfico e da tabela coincidem com os 20 maiores
  por `Sum(valor)` no `fato_repasses.csv`.
- A soma exata de seus saldos líquidos é **R$ 98.238.372,09**. Dividida pelo
  total de **R$ 288.699.999,97**, corresponde a **34,03%**.
- Na tabela, Porto Alegre tem R$ 16.247.674,42 em créditos e
  −R$ 10.465.116,28 em ajustes, chegando a R$ 5.782.558,14 líquidos.
- A seleção é parte essencial da leitura das capturas 03 e 05: nelas, o gráfico
  por pessoa mostra apenas os 20 municípios do marcador. Na captura 04, sem
  seleção, aparecem municípios da base completa.

## Limites da apresentação

O KPI e a coluna de participação da tabela aparecem arredondados em porcentagens
inteiras nas capturas. Os valores exatos constam na
[análise da task](../../task-17-concentracao.md). O título do gráfico por pessoa
refere-se a “20 maiores entre os 334” também quando o marcador está ativo;
nesse estado, a seleção exibida no topo da tela define o recorte real. Sem o
marcador, o gráfico mostra mais de 20 barras e permite rolagem. A captura 04
documenta o ranking completo, incluindo seus primeiros 20, e não um limite
fixo de 20 barras.
