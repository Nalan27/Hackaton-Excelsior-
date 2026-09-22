# Snapshot 07 — Task 14

## Conteúdo

Snapshot do aplicativo Qlik Cloud após a implementação da página
`Distribuição geográfica`:

- camada de pontos com tamanho por **Valor líquido recebido**;
- camada de áreas com cor por **Valor líquido recebido por pessoa**;
- filtros de recurso (`recurso`), mês (`mes_nome`) e município (`município`);
- tooltips com município, código IBGE, valor líquido, população 2024 e valor
  por pessoa;
- página da Task 15 (Linha do Tempo) preservada no mesmo aplicativo.

## Sequência do snapshot

O snapshot 06 pertence à Task 15. O snapshot 07 é a exportação seguinte do
aplicativo e registra a Task 14 sobre esse estado. A sequência representa a
ordem de exportação, não a ordem numérica das tasks ou telas.

## Arquivo

- Arquivo: `app.qvf`
- Ambiente: Qlik Cloud
- Exportação: 16/09/2026, com dados
- Responsável pelo versionamento: SallysMartins
- Tamanho: 393.216 bytes
- SHA-256: `B62100ED2CFC1DA4BF175CBDB7DE055750904A52DDE718DD977685882C2CC526`
- Armazenamento: Git LFS

O tamanho e o SHA-256 devem ser reconferidos após qualquer nova exportação do
aplicativo.

## Conferência dos dados

| Controle | Valor esperado |
|---|---:|
| Movimentações | 658 |
| Municípios recebedores | 334 |
| Valor líquido | R$ 288.699.999,97 |
| Ajustes negativos preservados | 18 |
| Porto Alegre — código IBGE | 4314902 |
| Porto Alegre — população 2024 | 1.389.322 |
| Porto Alegre — valor líquido | R$ 5.782.558,14 |
| Porto Alegre — valor por pessoa | R$ 4,16 |

Os valores foram confrontados com os CSVs de `data/processed/` e com os
tooltips do Qlik.

## Evidências visuais

As capturas, seleções e valores observados estão em
[`docs/evidencias/task-14/README.md`](../../../docs/evidencias/task-14/README.md).
A configuração e as limitações estão em
[`docs/task-14-tela-1.md`](../../../docs/task-14-tela-1.md).

## Dependências e restauração

O aplicativo usa:

- conexão `DataFiles`;
- script `qlik/load_data.qvs`;
- `dim_municipio.csv`;
- `fato_repasses.csv`;
- `dim_calendario.csv`;
- `intervalo_primeiro_repasse.csv`;
- medidas mestras da Task 12.

Para restaurar, importe `app.qvf` no Qlik Cloud. Para recarregar os dados,
envie os quatro CSVs à conexão `DataFiles` e valide o nome da conexão no editor
de carga.

Em 17/09/2026, Nalan27 confirmou que reimportou o snapshot e conferiu mapas,
filtros, tooltips e dados. O ambiente utilizado não foi registrado. Capturas
adicionais da visão geral mostram `Distribuição geográfica` entre as seis
pastas públicas da versão 07; a progressão desde os snapshots 05 e 06 está
documentada nas evidências da Task 14.

## Limitações

- O mapa cobre municípios recebedores, não todo o universo de municípios
  atingidos.
- O valor por pessoa usa a população estimada pelo IBGE/SIDRA para 2024.
- O indicador não mede impacto, necessidade ou adequação do repasse.

## Estado

Implementação e evidências preparadas para revisão no PR da Task 14.
