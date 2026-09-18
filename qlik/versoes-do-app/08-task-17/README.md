# Snapshot 08 — Task 17

Snapshot do aplicativo Qlik Cloud após a implementação da Tela 4 —
Concentração (H5). A exportação atual reúne a página geográfica do snapshot 07
e a Tela 4 da Task 17. O número **08** identifica a sequência de exportações do
aplicativo, não a ordem numérica das tasks ou telas.

## Conteúdo registrado

- pasta `Tela 4 — Concentração (H5)`;
- gráfico dos 20 maiores municípios por saldo líquido e marcador com a seleção
  desses municípios;
- tabela de créditos, ajustes negativos, saldo líquido, participação no total
  e valor por pessoa;
- gráfico de valor por pessoa, que responde ao marcador e à limpeza da seleção;
- KPI com o valor líquido da seleção e sua participação na base completa.
- página `Distribuição geográfica` da Task 14 preservada no mesmo aplicativo.

As [cinco evidências visuais](../../../docs/evidencias/task-17/README.md) e a
[metodologia com resultados](../../../docs/task-17-concentracao.md) acompanham
este snapshot. Uma captura adicional, fornecida na revisão em 17/09/2026,
mostra sete pastas públicas no Qlik, incluindo `Distribuição geográfica` e
`Tela 4 — Concentração (H5)`. A captura não está armazenada no repositório.

## Arquivo

- Arquivo: `app.qvf`
- Atualização informada: 17/09/2026, Qlik Cloud, com dados.
- Armazenamento no repositório: Git LFS (`*.qvf` em `.gitattributes`)
- Tamanho verificado: 393.216 bytes
- SHA-256 verificado: `27FFDDE1AA87AAC3733BCFE8BFA9B7C86EB4BF1F98FB8E349DF2E5F11A2BFCFF`

Nalan27 informou que conferiu o aplicativo consolidado e reimportou a nova
exportação. A captura mostra as páginas no Qlik, mas não permite verificar o
conteúdo binário do QVF nem o acesso sem credenciais.

## Dados e restauração

O aplicativo usa o script `qlik/load_data.qvs`, a conexão `DataFiles` e os CSVs
`dim_calendario.csv`, `fato_repasses.csv`, `dim_municipio.csv` e
`intervalo_primeiro_repasse.csv`. Para restaurar, importe `app.qvf` no Qlik
Cloud. Para recarregar, disponibilize os quatro CSVs na conexão `DataFiles` e
confira a conexão definida no script.
