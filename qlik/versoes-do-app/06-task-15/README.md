# Snapshot 06 — Task 15

## Conteúdo

Snapshot do app Qlik Cloud após a implementação da Tela 2 (Linha do Tempo — H2), conforme registrado pelo responsável pela exportação:

- pasta "Tela 2" com o gráfico "Evolução Mensal dos Repasses FUNDEC — Créditos, Ajustes e Saldo Líquido";
- três medidas reutilizáveis da Task #12: Ajustes Negativos, Créditos Recebidos e Valor Líquido Recebido;
- dimensão `ano_mes_ordem` (AAAAMM) para ordenar os meses cronologicamente;
- campo agregado `valor_pago` fora da análise transacional desta tela.

A numeração 06 segue a sequência de snapshots do app. Ela não representa a ordem de conclusão das tasks ou das demais telas.

## Arquivo

- Arquivo: `app.qvf`
- Exportação informada: 16/09/2026, Qlik Cloud, com dados
- Responsável pelo versionamento: John Victor E. Santo
- Tamanho informado: 360.448 bytes
- SHA-256 informado: `1405DAE92224168E41E79CA25FF5AB9A8A084913440ECADFDA145FF183775925`

## Conferência dos dados

O agrupamento do `data/processed/fato_repasses.csv` por mês da data confirma os cinco períodos de 2024-05 a 2024-09 e os totais abaixo:

| Medida | Total |
|---|---:|
| Créditos positivos | R$ 307.334.883,69 |
| Ajustes negativos | −R$ 18.634.883,72 |
| Saldo líquido | R$ 288.699.999,97 |

Essa conferência valida os totais da base usada como referência. A comparação visual com os valores mostrados pelo Qlik ainda precisa ser documentada com capturas do app.

## Evidências visuais

O primeiro print confirma que o eixo aparece na ordem 202405, 202406, 202407, 202408, 202409 e que as três medidas estão presentes no gráfico. O segundo mostra a seleção de julho (`ano_mes_ordem = 202407`) e a redução da visualização a esse mês.

As duas capturas e os valores mensais de referência estão em [`docs/evidencias/task-15/README.md`](../../../docs/evidencias/task-15/README.md):

1. `01-tela2-evolucao-mensal.png`: Tela 2 sem filtros, com os cinco meses e as três medidas;
2. `02-tela2-filtro.png`: Tela 2 com julho selecionado.

O gráfico mostra escala abreviada em milhões. As capturas permitem validar a apresentação e o efeito da seleção, mas não os valores exatos exibidos pelo Qlik. A conciliação numérica com as medidas da Task #12 depende de uma visualização ou exportação dos dados do gráfico com precisão completa. O rótulo numérico do eixo (por exemplo, 202406) também pode ser melhorado quanto à legibilidade antes da submissão final.

## Dependências e restauração

O app utiliza a conexão `DataFiles`, o script `qlik/load_data.qvs`, os CSVs `dim_calendario.csv`, `fato_repasses.csv`, `dim_municipio.csv` e `intervalo_primeiro_repasse.csv`, além das medidas mestras da Task #12.

Para restaurar, importe `app.qvf` no Qlik Cloud. Para uma nova recarga, envie os quatro CSVs à conexão `DataFiles` e confira a conexão usada pelo script.

## Estado

Implementação e evidências visuais entregues no snapshot 06. Conferência dos valores exatos exibidos pelo Qlik pendente antes da conclusão da Task #15.
