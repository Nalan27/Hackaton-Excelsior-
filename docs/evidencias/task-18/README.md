# Evidências da Task 18 — vulnerabilidade e repasses

| Captura | Estado e conferência visível |
|---|---|
| [Tela 5 sem filtros](./01-tela5-geral.png) | Gráfico de dispersão entre IDH-M 2010 e valor líquido por habitante, tabela municipal com código IBGE e valores formatados, além de nota sobre fontes, anos, cobertura e limites da interpretação. |

O ponto de **Coqueiro Baixo** está destacado no gráfico. A tabela permite
consultar cada município, inclusive **Pinto Bandeira**, cujo IDH-M é ausente.
Esses dois casos foram conferidos manualmente pelo usuário em 18/09/2026; a
captura geral não mostra suas linhas pesquisadas. Os números da análise
completa e o teste de sensibilidade por população podem ser reproduzidos com
[`etl/analise_idhm_repasses.py`](../../../etl/analise_idhm_repasses.py) e estão
explicados em [`docs/task-18-vulnerabilidade-repasses.md`](../../task-18-vulnerabilidade-repasses.md).

A nota do app apresenta as correlações calculadas **sem filtros**. Elas não se
recalculam quando o usuário seleciona municípios ou outros campos no Qlik. O
registro do QVF correspondente está no
[`snapshot 10`](../../../qlik/versoes-do-app/10-task-18/README.md).
