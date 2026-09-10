# Versão 01 — Task 09

- Arquivo: `app.qvf`
- Data da exportação: 10/09/2026
- Ambiente de origem: Qlik Cloud
- Tipo de exportação: com dados
- Responsável pelo versionamento: Nalan27
- Tamanho: 294.912 bytes
- SHA-256: `8AFA941C78817D31F6FE769872C16C76AC8EA85988EDCD38DB9E45F1772D372E`

## Alterações

Snapshot do app após a implementação da Task 09 — dimensão calendário.

## Dependências

- Conexão de dados `DataFiles` no Qlik Cloud.
- Arquivos `dim_municipio.csv`, `fato_repasses.csv` e
  `dim_calendario.csv`, disponíveis em `data/processed/`.
- Script de carga disponível em `qlik/load_data.qvs`.
- Não há extensões ou temas externos documentados para esta versão.

## Restauração

1. Faça upload de `app.qvf` no Qlik Cloud.
2. O snapshot já contém os dados carregados no momento da exportação.
3. Para uma nova recarga, envie os três CSVs para a conexão `DataFiles` e
   confirme ou ajuste a conexão usada pelo script.
4. Valide os totais descritos em
   `docs/task-9-calendario.md`.
