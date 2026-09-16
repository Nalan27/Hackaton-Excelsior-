# Snapshot 08 — Task 17

Snapshot do aplicativo Qlik Cloud após a implementação da Tela 4 —
Concentração (H5). O número **08** identifica a sequência de exportações do
aplicativo. O snapshot 07 está sendo preparado por outro integrante e será
submetido em PR próprio; a numeração não é a ordem de conclusão das issues.

## Conteúdo registrado

- pasta `Tela 4 — Concentração (H5)`;
- gráfico dos 20 maiores municípios por saldo líquido e marcador com a seleção
  desses municípios;
- tabela de créditos, ajustes negativos, saldo líquido, participação no total
  e valor por pessoa;
- gráfico de valor por pessoa, que responde ao marcador e à limpeza da seleção;
- KPI com o valor líquido da seleção e sua participação na base completa.

As [cinco evidências visuais](../../../docs/evidencias/task-17/README.md) e a
[metodologia com resultados](../../../docs/task-17-concentracao.md) acompanham
este snapshot. As capturas documentam o estado observado no Qlik; a integridade
do conteúdo interno do QVF não foi verificada por reimportação nesta revisão.

## Arquivo

- Arquivo: `app.qvf`
- Exportação informada: 16/09/2026, Qlik Cloud. A presença dos dados embutidos
  e a restauração devem ser confirmadas em uma importação de teste.
- Armazenamento no repositório: Git LFS (`*.qvf` em `.gitattributes`)
- Tamanho verificado: 360.448 bytes
- SHA-256 verificado: `BD62C0409F08B550AAAE0063C8D0475902C6A44DA959D4FA4A23E87CA32087B3`

O arquivo tem hash diferente do snapshot 06. Ao integrar o PR do snapshot 07,
convém conferir no Qlik se este arquivo também contém as alterações daquele
snapshot antes de usá-lo como versão consolidada do aplicativo.

## Dados e restauração

O aplicativo usa o script `qlik/load_data.qvs`, a conexão `DataFiles` e os CSVs
`dim_calendario.csv`, `fato_repasses.csv`, `dim_municipio.csv` e
`intervalo_primeiro_repasse.csv`. Para restaurar, importe `app.qvf` no Qlik
Cloud. Para recarregar, disponibilize os quatro CSVs na conexão `DataFiles` e
confira a conexão definida no script.
