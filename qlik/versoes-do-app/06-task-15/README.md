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

## Validação visual pendente

O responsável informou que o eixo aparece na ordem 202405, 202406, 202407, 202408, 202409 e que o saldo líquido coincide com as telas "Validação do calendário" (Task #9) e "Visão Geral" (Task #13). O PR #40 ainda não contém os prints necessários para confirmar essas observações durante a revisão.

Adicionar em `docs/evidencias/task-15/`:

1. `01-tela2-evolucao-mensal.png`: Tela 2 em modo de visualização, sem filtros, com os cinco meses e as três medidas visíveis;
2. uma captura com seleção de mês ou município para mostrar o comportamento dos filtros;
3. um `README.md` que explique o que cada imagem confirma.

Após incluir as capturas, atualizar esta seção com os nomes reais dos arquivos e os valores conferidos no Qlik. O rótulo numérico do eixo (por exemplo, 202406) também deve ser avaliado quanto à legibilidade antes da submissão final.

## Dependências e restauração

O app utiliza a conexão `DataFiles`, o script `qlik/load_data.qvs`, os CSVs `dim_calendario.csv`, `fato_repasses.csv`, `dim_municipio.csv` e `intervalo_primeiro_repasse.csv`, além das medidas mestras da Task #12.

Para restaurar, importe `app.qvf` no Qlik Cloud. Para uma nova recarga, envie os quatro CSVs à conexão `DataFiles` e confira a conexão usada pelo script.

## Estado

Implementação entregue no snapshot 06; confirmação visual pendente no PR #40. A revisão final da Task #15 depende dos prints do Qlik.
