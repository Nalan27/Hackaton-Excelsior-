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
- Armazenamento no repositório: Git LFS
- Exportação informada: 16/09/2026, Qlik Cloud, com dados
- Responsável pelo versionamento: John Victor E. Santo
- Tamanho verificado: 360.448 bytes
- SHA-256 verificado: `1405DAE92224168E41E79CA25FF5AB9A8A084913440ECADFDA145FF183775925`

## Conferência dos dados

O agrupamento do `data/processed/fato_repasses.csv` por mês da data confirma os cinco períodos de 2024-05 a 2024-09 e os totais abaixo:

| Medida | Total |
|---|---:|
| Créditos positivos | R$ 307.334.883,69 |
| Ajustes negativos | −R$ 18.634.883,72 |
| Saldo líquido | R$ 288.699.999,97 |

As cinco linhas da visão de dados do Qlik foram confrontadas com esta base e coincidem nas três medidas. Os totais foram obtidos pela soma das linhas; a tabela do Qlik não exibe uma linha de total.

## Evidências visuais

O primeiro print confirma que o eixo aparece na ordem 202405, 202406, 202407, 202408, 202409 e que as três medidas estão presentes no gráfico. O segundo mostra a seleção de julho (`ano_mes_ordem = 202407`) e a redução da visualização a esse mês. O terceiro mostra os valores completos das três medidas para cada mês, sem seleção.

As duas capturas e os valores mensais de referência estão em [`docs/evidencias/task-15/README.md`](../../../docs/evidencias/task-15/README.md):

1. `01-tela2-evolucao-mensal.png`: Tela 2 sem filtros, com os cinco meses e as três medidas;
2. `02-tela2-filtro.png`: Tela 2 com julho selecionado;
3. `03-tela2-dados-mensais.png`: visão de dados do gráfico, com os valores completos dos cinco meses.

O gráfico mostra escala abreviada em milhões, mas a terceira captura permite validar os valores exatos exibidos pelo Qlik e conciliá-los com as medidas da Task #12. O rótulo numérico do eixo (por exemplo, 202406) pode ser melhorado quanto à legibilidade antes da submissão final.

## Dependências e restauração

O app utiliza a conexão `DataFiles`, o script `qlik/load_data.qvs`, os CSVs `dim_calendario.csv`, `fato_repasses.csv`, `dim_municipio.csv` e `intervalo_primeiro_repasse.csv`, além das medidas mestras da Task #12.

Para restaurar, importe `app.qvf` no Qlik Cloud. Para uma nova recarga, envie os quatro CSVs à conexão `DataFiles` e confira a conexão usada pelo script.

## Estado

Implementação e três evidências visuais entregues no snapshot 06. Valores mensais exibidos pelo Qlik conferidos com a base processada. Pronto para revisão no PR #40.
