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
[`snapshot 09`](../../../qlik/versoes-do-app/09-task-16/README.md). Também
confirmou a correção do KPI de 334 municípios na Visão Geral e apresentou o
mapa de áreas da Task 14 novamente preenchido.

As capturas estão arquivadas nesta pasta:

| Captura | O que permite conferir |
|---|---|
| [Tela 3 sem seleção](./01-tela3-geral.png) | KPIs 478 / 334 / 144, filtros, tabela e nota com os dois períodos. |
| [Afetados sem registro](./02-afetados-sem-registro.png) | Seleção `afetado_sem_registro`, KPIs 144 / 0 / 144 e exemplos com zero movimentações. |
| [Modelo de dados](./03-validacao-modelo.png) | Uma tabela `cobertura_municipal` ligada por `chave_municipal`, sem `$Syn` visível. |

Nas duas capturas da Tela 3, o objeto é uma tabela dinâmica com dimensões
recolhidas. Código IBGE e classificação não aparecem diretamente nas linhas;
para auditar os casos no app, é preciso expandi-las ou exibir esses campos em
colunas de uma tabela simples. Os CSVs vinculados acima permitem a conferência
por código.

O arquivo QVF foi verificado por tamanho e SHA-256, mas ainda não foi
reimportado para testar a restauração. A [análise da Task 16](../../task-16-cobertura-lacunas.md)
explica por que ausência de registro não equivale a ausência de atendimento ou
de elegibilidade.
