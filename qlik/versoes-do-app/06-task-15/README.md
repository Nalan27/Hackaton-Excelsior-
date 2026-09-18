<<<<<<< HEAD
Versão 06 — Task 15

- Arquivo: app.qvf 
- Data da exportação: 16/09/2026
- Ambiente de origem: Qlik Cloud
- Tipo da exportação: com dados
- Responsável pelo versionamento: John Victor E. Santo
- Tamanho: 360.448 bytes
- SHA-256: 1405DAE92224168E41E79CA25FF5AB9A8A084913440ECADFDA145FF183775925

Alterações
Snapshot do app após a implementação da Task 15 — Linha do Tempo (H2):

- criação da pasta "Tela 2", com o gráfico de barras "Evolução Mensal dos Repasses FUNDEC — Créditos, Ajustes e Saldo Líquido";
- gráfico usa as três medidas reutilizáveis da Task #12 (Ajustes Negativos, Créditos Recebidos, Valor Líquido Recebido), sem reescrever expressões soltas;
- dimensão configurada como `ano_mes_ordem` (campo numérico inteiro da dim_calendario, formato AAAAMM) em vez de `ano_mes`, corrigindo a ordenação cronológica que saía fora de sequência nas validações anteriores;
- campo `valor_pago` (oriundo do ranking agregado por município, em dim_municipio) não foi incluído nesta tela, evitando misturar granularidade transacional com granularidade agregada.

Validação
- Eixo temporal exibe os períodos em ordem cronológica correta: 202405, 202406, 202407, 202408, 202409 — confirmado em modo de visualização.
- Total líquido bate com o conciliado na Task #12: Créditos Recebidos (R$ 307.334.883,69) + Ajustes Negativos (–R$ 18.634.883,72) = Valor Líquido Recebido (R$ 288.699.999,97), conferido linha a linha por período.
- Mesmo total (R$ 288.699.999,97 / 288,7M) confirmado de forma independente na pasta "Validação do calendário" (Task 9, via Sum(valor)) e na pasta "Visão Geral" (Task 13, KPI Total Repassado) — consistência de ponta a ponta no app.
- 5 períodos cobertos: 2024-05 a 2024-09.

Observação de melhoria (não bloqueante)
O rótulo do eixo usa o formato numérico puro (ex. "202406"), sem separador. É funcional e correto, mas menos legível que um formato "jun/2024" ou "2024-06". Fica como sugestão de polimento visual para antes da submissão, não como pendência de correção.

Dependências
- conexão DataFiles no Qlik Cloud;
- dim_calendario.csv;
- fato_repasses.csv;
- dim_municipio.csv;
- intervalo_primeiro_repasse.csv;
- script de carga qlik/load_data.qvs;
- medidas mestras publicadas na Task #12 (Ajustes Negativos, Créditos Recebidos, Valor Líquido Recebido).

Restauração
- Importe app.qvf no Qlik Cloud.
- O snapshot já contém os dados carregados no momento da exportação.
- Para uma nova recarga, envie os quatro CSVs para a conexão DataFiles e confirme ou ajuste a conexão usada pelo script.

Evidências visuais: docs/evidencias/task-15/.

| Arquivo | Descrição |
|---|---|
| 01-tela2-evolucao-mensal.png | Gráfico de barras da Tela 2 em modo de visualização, com os três períodos-chave (202406 como pico de créditos, 202407 como maior ajuste negativo) |

Estado
Concluído e validado.
=======
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
>>>>>>> origin/main
