# Snapshot 09 — Task 16

Snapshot do aplicativo Qlik Cloud após a criação da **Tela 3 — Cobertura e
lacunas (H4)**. A sequência 09 identifica a ordem de exportação do app; o
snapshot anterior é o 08 da Task 17.

## Conteúdo informado e conferido

- carga de `cobertura_municipal.csv` ligada ao modelo por `chave_municipal`, sem
  chave sintética após a remoção da carga duplicada;
- três KPIs da Tela 3: 478 municípios na lista da Defesa Civil, 334 com
  movimentação na base FUNDEC e 144 sem registro nessa base;
- tabela com município, código IBGE, situação, quantidade de movimentações e
  saldo líquido, além de filtros e nota sobre períodos e limites;
- medida **Municípios atendidos** da Visão Geral ajustada para
  `Count(DISTINCT municipio_ibge_2024)`; valor sem filtros de 334;
- gráficos da Tela 4 e mapa de áreas da página geográfica restaurados após a
  correção da ordem da seção `Normalização` e da dimensão `localizacao_mapa`.

O usuário relatou a validação desses elementos no Qlik em 17/09/2026. Os
prints compartilhados na revisão não foram salvos no repositório; os controles
reproduzíveis estão em
[`docs/evidencias/task-16/README.md`](../../../docs/evidencias/task-16/README.md).

## Arquivo

- Arquivo: `app.qvf`.
- Exportação informada: 17/09/2026, Qlik Cloud, **com dados**.
- Tamanho verificado: **425.984 bytes**.
- SHA-256 verificado: `EDE8B028F98E12F9240209C79103F45C0C836F73DB7AF45A77CFCFFDE04D9452`.
- Armazenamento: Git LFS (`*.qvf` em `.gitattributes`).

O tamanho e o hash identificam o arquivo recebido; não comprovam sozinhos que
o QVF foi exportado com dados nem que pode ser restaurado. A **reimportação do
snapshot 09 ainda precisa ser confirmada**.

## Dados e restauração

Para abrir o snapshot, importe `app.qvf` no Qlik Cloud. Para executar uma nova
recarga, disponibilize na conexão `DataFiles` os cinco CSVs
`dim_municipio.csv`, `fato_repasses.csv`, `dim_calendario.csv`,
`intervalo_primeiro_repasse.csv` e `cobertura_municipal.csv`. O bloco de carga
da cobertura está em [`qlik/load_data.qvs`](../../load_data.qvs).

Mantenha apenas uma carga de `cobertura_municipal.csv`. Se a dimensão municipal
usar os comandos `RENAME FIELD` da seção `Normalização`, posicione essa seção
após a seção gerada automaticamente. Confira no modelo uma única ligação por
`chave_municipal`, sem `$Syn`, e valide os KPIs **478 / 334 / 144**.

## Limite da análise

A lista da Defesa Civil é um extrato de 11/06/2024; a base FUNDEC analisada vai
até 26/09/2024. Os 144 casos são municípios da lista sem movimentação **nesta
base**, não municípios comprovadamente sem assistência. Método e resultados:
[`docs/task-16-cobertura-lacunas.md`](../../../docs/task-16-cobertura-lacunas.md).
