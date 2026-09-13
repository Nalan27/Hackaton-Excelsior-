# Versão 02 — Task 10

- Arquivo: `app.qvf`
- Data da exportação: 13/09/2026
- Ambiente de origem: Qlik Cloud
- Tipo da exportação: com dados
- Responsável pelo versionamento: equipe Hackaton Excelsior
- Tamanho: 327.680 bytes
- SHA-256: `927B58199FB12B03D03CE9D9660469AB1B47779DD78E8F2752C005D33F43C8F3`

## Alterações

Snapshot do app após a implementação da Task 10:

- carga da tabela `intervalo_primeiro_repasse`;
- associação por `chave_municipal`;
- pasta `Validação do primeiro repasse`;
- KPIs de cobertura, menor intervalo, mediana e maior intervalo.

## Validação

| Indicador | Resultado |
|---|---:|
| Municípios com intervalo válido | 334 |
| Menor intervalo | 23 dias |
| Intervalo mediano | 28 dias |
| Maior intervalo | 135 dias |

A recarga terminou com quatro tabelas, nenhuma tabela sem associação e
nenhuma recomendação pendente. O modelo não apresentou chave sintética nem
associação circular.

## Dependências

- conexão `DataFiles` no Qlik Cloud;
- `dim_municipio.csv`;
- `fato_repasses.csv`;
- `dim_calendario.csv`;
- `intervalo_primeiro_repasse.csv`;
- script de carga `qlik/load_data.qvs`.

## Restauração

1. Importe `app.qvf` no Qlik Cloud.
2. O snapshot já contém os dados carregados no momento da exportação.
3. Para uma nova recarga, envie os quatro CSVs para `DataFiles`.
4. Confirme ou ajuste a conexão utilizada por `qlik/load_data.qvs`.
5. Valide os resultados descritos em
   `docs/task-10-intervalo-primeiro-repasse.md`.
