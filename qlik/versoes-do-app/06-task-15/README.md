Versão 06 — Task 15

Arquivo: app.qvf
Data da exportação: 16/09/2026
Ambiente de origem: Qlik Cloud
Tipo da exportação: com dados
Responsável pelo versionamento: equipe Hackaton Excelsior
Tamanho: 360.448 bytes
SHA-256: 1405DAE92224168E41E79CA25FF5AB9A8A084913440ECADFDA145FF183775925

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
