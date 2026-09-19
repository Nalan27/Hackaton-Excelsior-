# Issue #20 — revisão de usabilidade do app Qlik

## Escopo e estado

Revisão iniciada em 19/09/2026 sobre o [snapshot 11](../../../qlik/versoes-do-app/11-task-19/README.md), as [capturas arquivadas das Telas 0 a 6](../../screenshots/tela-6-resumo/) e sete novas capturas sem filtros enviadas na conversa em 19/09. As capturas arquivadas são do aplicativo antes da exportação de 18/09. As primeiras capturas novas mostram a cópia do app após a limpeza das pastas de teste; capturas posteriores registram correções parciais nas Telas 0 e 1. Falta testar a cópia usada nos prints e no pitch, aplicar as correções abaixo e exportar um **novo QVF com dados**. Este documento não atesta a conclusão da issue.

## O que foi feito até agora

- A revisão visual das sete telas foi iniciada com as capturas recebidas em 19/09. Os totais da Tela 0 foram comparados com a validação do ETL e permanecem corretos.
- Na cópia do Qlik em revisão, as três pastas de desenvolvimento foram retiradas da lista pública; uma nova captura mostra as sete telas de apresentação na ordem 0–6. As pastas de teste permanecem preservadas nos snapshots anteriores.
- A Tela 0 recebeu rótulos que explicitam o saldo líquido e o universo de municípios com repasse, além de nota com população IBGE/SIDRA 2024, marco de 24/04/2024 e arredondamento do tempo médio. Uma nova captura confirmou o resultado visual sem filtros.
- Na Tela 1, o filtro de meses foi ordenado cronologicamente e as dimensões dos mapas passaram a aparecer como “Município”. O reteste com Porto Alegre mostrou o mapa de pontos em escala regional, além de tooltip com código IBGE 4314902, saldo líquido de R$ 5.782.558,14 e população de 1.389.322. O quociente por pessoa é R$ 4,16, mas aparece como `R$4.16` no tooltip. A legenda de cor ainda mostra um intervalo sem amplitude quando só essa cidade está selecionada.

As capturas novas foram enviadas na conversa de revisão e **ainda não estão arquivadas no repositório**. O snapshot 11 continua sendo o último QVF versionado; ele não comprova as alterações feitas depois de 18/09.

## O que falta para concluir a issue

- Finalizar a Tela 1: escala de cores ao filtrar, legibilidade das duas legendas, formatação `pt-BR` do valor por pessoa no tooltip e nota de fonte/período; guardar capturas após correção.
- Aplicar e retestar os pontos das Telas 2 a 6 descritos abaixo, sem alterar os cálculos validados.
- Executar o roteiro interativo completo, incluindo navegação entre telas com filtros, caso sem movimentação e confronto de KPI, mapa e timeline com os totais de referência.
- Arquivar os prints finais em modo de análise, exportar o novo QVF **com dados**, registrar sua identificação e verificar a versão usada no documento e no pitch antes de 23/09/2026.

## Controles já sustentados por evidências anteriores

| Controle | Resultado | Evidência |
|---|---:|---|
| Total líquido sem filtros / municípios recebedores | R$ 288.699.999,97 / 334 | [validação do ETL](../../../data/processed/relatorio_validacao.csv), [Tela 0](../../screenshots/tela-6-resumo/tela-0-visao-geral.png) |
| Porto Alegre no mapa | R$ 5.782.558,14; 1.389.322 habitantes; R$ 4,16/pessoa | [Task 14](../task-14/README.md) |
| Julho de 2024 na timeline | créditos R$ 80.289.534,88; ajustes −R$ 11.565.116,28; líquido R$ 68.724.418,60 | [Task 15](../task-15/README.md) |
| Cobertura sem filtros | 478 listados; 334 com movimentação; 144 sem registro | [Task 16](../task-16/README.md) |
| Top 20 por saldo líquido | R$ 98.238.372,09; 34,03% do total | [Task 17](../task-17/README.md) |

Os filtros de recurso, mês e município foram testados em versões anteriores nas [Tasks 13](../task-13/README.md), [14](../task-14/README.md) e [15](../task-15/README.md). Esses testes não substituem o reteste do QVF final.

## Ajustes identificados nas capturas

| Tela | Achado observável | Ajuste e reteste esperado |
|---|---|---|
| 0 — Visão Geral | Na primeira captura, “Total Repassado” e “Cidades Contempladas” eram ambíguos; a nota não informava o ano da população nem o marco da espera. | **Reteste visual em 19/09:** nova captura mostra “Total líquido repassado”, “Municípios com repasse na base”, população IBGE/SIDRA 2024 e marco 24/04/2024. Os quatro valores continuam R$ 288.699.999,97 / 334 / R$ 32,89 / 40 dias. Falta retestar filtros no QVF final. |
| 1 — Distribuição geográfica | A primeira captura mostrava `Mês` em ordem alfabética, `localizacao_mapa` e números em formato inglês. **Retestes parciais:** meses e rótulo “Município” corrigidos; com Porto Alegre selecionado, o ponto agora aparece em escala regional e o tooltip confirma código IBGE 4314902, R$ 5.782.558,14 e população 1.389.322. O tooltip exibe `R$4.16` em vez de `R$ 4,16`; o valor máximo da legenda de pontos fica truncado e a legenda de áreas indica `R$ 4,16 – < R$ 4,16` ao restar uma cidade. | Formatar o valor por pessoa do tooltip em `pt-BR`. No mapa de pontos, usar “Saldo líquido (R$ milhões)” com valores como `5,78`; se necessário, `Sum(valor)/1000000` só em “Dimensionar por”, preservando o valor exato no tooltip. No mapa de áreas, testar escala de cor fixa de 0 a 1018.22 (máximo per capita na base completa), rótulo “R$ por pessoa” e números com duas casas sem repetir `R$` em cada faixa. Incluir nota de fonte, período e população 2024. Retestar os dois mapas sem filtro e com filtros de município, mês e recurso. |
| 2 — Linha do Tempo | Eixo mostra `ano_mes_ordem` e `202405`–`202409`; o eixo de valores não explicita R$. | Exibir `mai/2024`–`set/2024` em ordem cronológica e informar que a escala é em reais. Se trocar a dimensão, confirmar novamente as cinco linhas mensais e o filtro de julho. Uma opção no Qlik é usar a dimensão calculada `=Dual(Date(MakeDate(Floor(ano_mes_ordem/100), Mod(ano_mes_ordem,100), 1), 'MMM/YYYY'), ano_mes_ordem)` e ordenar pelo valor numérico. |
| 3 — Cobertura | O texto provisório `Clique para incluir um título` não aparece mais na captura atual, mas a tabela continua sem título descritivo e mostra códigos como `nao_listado_sem_registro`. | Dar título à tabela e apresentar classificações legíveis, mantendo os códigos originais na base. Conferir que 478 / 334 / 144 continuam iguais. |
| 4 — Concentração | O título “20 maiores valores por pessoa entre os 334 municípios” permanece mesmo quando o marcador reduz a amostra a 20; sem marcador, o gráfico permite rolar por mais de 20 barras. O KPI de 288,7M e 100% aparece apertado. | Usar um título válido em ambos os estados, por exemplo “Ranking de R$ por pessoa — conforme filtros”; ajustar o espaço/formatação do KPI. Testar com e sem marcador; com marcador, conferir R$ 98.238.372,09 e 34,03%. |
| 5 — Vulnerabilidade | O texto provisório `Clique para incluir um título` não aparece mais na captura atual; a tabela está sem título descritivo. | Nomear a tabela; conferir que o gráfico mantém 333 municípios comparáveis e a nota de fonte/anos. |
| 6 — Resumo | O título do KPI por pessoa está truncado e o total usa `288.7M`, fora do padrão `pt-BR` das outras telas. | Encurtar ou redimensionar o título; usar valor em reais legível, preferencialmente `R$ 288,70 mi` ou o valor exato. Conferir também R$ 32,89 e o ajuste de julho. |
| Navegação | Uma primeira captura da visão de pastas enviada em 19/09 mostrava dez pastas: as sete telas de apresentação e, antes delas, `Validação do calendário`, `Mapa de teste` e `Validação do primeiro repasse`. A Tela 2 aparecia antes da página geográfica. | **Reteste parcial:** segunda captura enviada em 19/09 mostra apenas sete pastas públicas, na ordem Visão Geral, Distribuição geográfica, Linha do Tempo, Cobertura e lacunas, Concentração, Vulnerabilidade, Resumo; `Meus próprios (0)`. Falta percorrer as sete telas com seleções limpas e com uma seleção ativa. Os snapshots anteriores preservam as páginas de teste. |

Os ajustes de texto da Tela 0 aparecem na nova captura enviada em 19/09, mas a tela ainda precisa de reteste interativo. Conferir também se as Telas 1, 2, 4 e 6 mostram ou remetem claramente às fontes, ao período e às unidades sem depender da explicação oral do pitch. A Tela 5 identifica fontes e anos.

## Roteiro de teste da versão final

Fazer em modo de análise, em janela de tamanho semelhante ao dos prints e sem painéis de edição abertos. Guardar capturas dos resultados e anotar a data, o responsável e a identificação do app/QVF.

1. **Sem seleções:** percorrer as Telas 0–6 pelas setas ou menu. Verificar ordem, títulos, legibilidade, fontes, período, unidades, tooltips e ausência de erro visual. Na Tela 0, conferir R$ 288.699.999,97, 334, R$ 32,89 e 40 dias arredondados. Na Tela 3, conferir 478 / 334 / 144.
2. **Município:** selecionar Porto Alegre na Tela 0 ou 1 e visitar as demais telas sem limpar a seleção. No mapa, conferir R$ 5.782.558,14, população 1.389.322 e R$ 4,16/pessoa; conferir que o recorte exibido nas outras telas é coerente. Limpar a seleção e verificar retorno aos totais globais.
3. **Mês:** selecionar julho de 2024 na Tela 2. Conferir créditos R$ 80.289.534,88, ajustes −R$ 11.565.116,28 e saldo R$ 68.724.418,60; visitar a Tela 1 e verificar a atualização dos dois mapas. Limpar a seleção.
4. **Marcador Top 20:** na Tela 4, aplicar o marcador e confirmar 20 municípios, R$ 98.238.372,09 e 34,03%; observar se título, gráfico por pessoa, tabela e KPI descrevem o mesmo recorte. Remover o marcador.
5. **Sem movimentação:** na Tela 3, selecionar Aceguá (`4300034`), listado no extrato, sem movimentações FUNDEC nesta base. Confirmar zero/ausência de registros sem erro ou indicação enganosa; navegar para mapa e timeline e registrar como cada objeto comunica o estado vazio. Se a seleção de Aceguá não se propagar às demais telas, registrar esse comportamento e testar outro recorte sem dados disponível no aplicativo.
6. **Capturas e pitch:** repetir a navegação no **mesmo app** que será gravado, com seleções limpas ao iniciar. Fazer os prints finais em modo de análise, atualizar o relatório com essas imagens e exportar `qlik/versoes-do-app/12-task-20/app.qvf` **com dados**. Registrar tamanho, SHA-256, data, responsável e o resultado dos testes no README do novo snapshot.

Repetir uma inspeção breve em 21/09 e uma conferência final até 23/09/2026, como previsto na issue. Problemas encontrados devem ter captura antes/depois e resultado do reteste; só então marcar os critérios da [issue #20](https://github.com/Nalan27/Hackaton-Excelsior-/issues/20).

## Referências de configuração Qlik

- [Expressão `Dual()` para texto legível com ordenação numérica](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/Scripting/FormattingFunctions/Dual.htm).
- [Títulos, subtítulos e notas de visualização](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/Visualizations/change-appearance-of-visualization.htm).
- [Navegação entre pastas](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/Sheets/navigating-sheets.htm).
