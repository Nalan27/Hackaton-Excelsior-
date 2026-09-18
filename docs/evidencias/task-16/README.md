# Evidências da Task 16 — cobertura e lacunas

## Controles reproduzíveis

| Controle | Resultado | Artefato |
|---|---:|---|
| Municípios do RS | 497 | [`cobertura_municipal.csv`](../../../data/processed/cobertura_municipal.csv) |
| Municípios no extrato da Defesa Civil | 478 | [`municipios_afetados_defesa_civil_2024_06_11.csv`](../../../data/processed/municipios_afetados_defesa_civil_2024_06_11.csv) |
| Listados com movimentação na base completa | 334 | [`relatorio_cobertura.csv`](../../../data/processed/relatorio_cobertura.csv) |
| Listados sem movimentação nessa base | 144 | [`casos_cobertura_investigacao.csv`](../../../data/processed/casos_cobertura_investigacao.csv) |
| Listados com movimentação até a data do extrato | 237 | [`relatorio_cobertura.csv`](../../../data/processed/relatorio_cobertura.csv) |

Casos de conferência na tabela do Qlik: Aceguá (`4300034`) consta na lista e
tem zero movimentações nesta base; Agudo (`4300109`) consta na lista, tem três
movimentações e saldo líquido de R$ 1.858.139,53; Arroio do Sal (`4301057`)
não consta no extrato e não tem movimentações na base. Os 19 municípios não
listados no extrato também não têm registros nessa base.

## Evidência do aplicativo

Em 17/09/2026, o usuário informou que a Tela 3 mostrou os KPIs **478 / 334 /
144**, acrescentou a tabela e os filtros, conferiu os casos indicados e
exportou o app com dados no
[`snapshot 09`](../../../qlik/versoes-do-app/09-task-16/README.md). Em
18/09/2026, substituiu a tabela dinâmica por uma tabela simples e exportou o
[`snapshot 10`](../../../qlik/versoes-do-app/10-task-18/README.md) junto com a
Tela 5.

As capturas estão arquivadas nesta pasta:

| Captura | O que permite conferir |
|---|---|
| [Tela 3 sem seleção](./01-tela3-geral.png) | KPIs 478 / 334 / 144, tabela simples com código IBGE e classificações visíveis, além da nota com os dois períodos. As primeiras linhas estão ordenadas pela classificação e mostram municípios fora da lista. |
| [Afetados sem registro](./02-afetados-sem-registro.png) | Seleção `afetado_sem_registro`, KPIs 144 / 0 / 144 e linhas com zero movimentações e saldo R$ 0,00. |
| [Modelo de dados](./03-validacao-modelo.png) | Captura anterior da única tabela `cobertura_municipal` ligada por `chave_municipal`, sem `$Syn` visível. |

Nas capturas atuais da Tela 3, município, código IBGE, comparação com a lista,
situação na base, quantidade de movimentações e saldo aparecem diretamente em
colunas. A primeira captura mostra também municípios **fora** da lista de
afetados; o KPI de 144 refere-se apenas aos **listados** sem registro, isolados
na segunda captura. Os CSVs vinculados acima permitem a conferência por código.

O QVF do snapshot 10 foi verificado por tamanho e SHA-256. Em 18/09/2026, o
usuário confirmou a reimportação e informou que o app estava correto; não há
captura separada da cópia reimportada. A [análise da Task 16](../../task-16-cobertura-lacunas.md)
explica por que ausência de registro não equivale a ausência de atendimento ou
de elegibilidade.
