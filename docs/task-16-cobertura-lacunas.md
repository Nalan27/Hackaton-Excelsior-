# Task 16 — Tela 3: cobertura e lacunas (H4)

## Pergunta e recorte

Quais municípios da **lista de afetados da Defesa Civil do RS em 11/06/2024**
aparecem na base detalhada de movimentações do FUNDEC/RS versionada neste
projeto? A lista identifica municípios afetados até aquele extrato; **não
define elegibilidade ao FUNDEC**, intensidade do dano ou pessoas atingidas.

| Fonte | Recorte | Artefato |
|---|---|---|
| [Defesa Civil do RS — relação de municípios afetados](https://estado.rs.gov.br/upload/arquivos/202407/municipios-afetados-defesa-civil-8-7-2024.pdf) | Extrato gerado em **11/06/2024 às 10:06**, com 478 municípios | [`PDF preservado`](../data/raw/pdf/defesa-civil-rs-municipios-afetados-2024-06-11.pdf) |
| [IBGE/SIDRA, tabela 6579](https://sidra.ibge.gov.br/tabela/6579) | 497 municípios do RS, nomes e códigos IBGE usados no projeto | [`populacao_rs_2024.csv`](../data/raw/csv/populacao_rs_2024.csv) |
| Movimentações detalhadas FUNDEC/RS | 658 linhas entre **17/05/2024 e 26/09/2024** | [`fato_repasses.csv`](../data/processed/fato_repasses.csv) |

O nome da URL do PDF menciona `8-7-2024`, mas o próprio documento informa
**11/06/2024 10:06** como data do extrato. A análise usa a data impressa no
documento. O arquivo PDF versionado foi separado da resposta do servidor, que
incluía avisos e HTML antes e depois do conteúdo PDF. Seu SHA-256 é
`9407C21EC0318B51035A82C7D615BDD97253CA582A34B7A50B310BCE4B75F5FB`.

## Método reproduzível

Execute, a partir da raiz do repositório:

```powershell
.\.venv\Scripts\python.exe etl/analis_de_dados.py
.\.venv\Scripts\python.exe etl/cobertura_municipal.py
```

Instale antes as dependências de `requirements.txt`, se necessário. O segundo
script extrai os 478 nomes do PDF, exige a sequência completa de itens e
associa cada nome a um código IBGE de sete dígitos usando a lista dos 497
municípios do RS. A normalização remove acentos e apóstrofos, permitindo
conciliar `Santana do Livramento` da Defesa Civil com `Sant'Ana do Livramento`
do IBGE (código `4317103`). O script interrompe a execução se houver nome sem
código, código duplicado ou repasse fora do cadastro municipal do RS.

Arquivos gerados em `data/processed/`:

| Arquivo | Conteúdo |
|---|---|
| `municipios_afetados_defesa_civil_2024_06_11.csv` | 478 nomes da fonte, ordem original e código IBGE associado. |
| `cobertura_municipal.csv` | 497 municípios, presença na lista, movimentações, créditos, ajustes, saldo líquido e classificação. |
| `casos_cobertura_investigacao.csv` | Casos que merecem revisão: afetado sem registro na base, não listado com registro ou saldo zero com movimentação. |
| `relatorio_cobertura.csv` | Contagens de controle e datas dos dois recortes. |

`sem_registro` significa zero linhas em `fato_repasses.csv` no período da base.
`saldo_zero` exige pelo menos uma movimentação cuja soma seja zero. Créditos e
ajustes negativos permanecem com seus sinais. O script calcula também as
movimentações até 11/06/2024 para mostrar o efeito da diferença entre as datas
das fontes. A tabela fato possui apenas a data, sem hora; por isso, o recorte
inclui todo o dia 11/06, mesmo que o extrato tenha sido gerado às 10:06.
**Nenhuma dessas categorias equivale a “sem atendimento”.**

## Resultado com a base versionada

| Controle | Resultado |
|---|---:|
| Municípios do RS no cadastro IBGE | 497 |
| Municípios no extrato de afetados | 478 |
| Movimentações detalhadas FUNDEC | 658 |
| Saldo líquido das movimentações | R$ 288.699.999,97 |
| Municípios com movimentação FUNDEC na base completa | 334 |
| Listados como afetados com movimentação até 26/09/2024 | 334 |
| Listados como afetados sem movimentação até 26/09/2024 | 144 |
| Listados como afetados com movimentação até 11/06/2024 | 237 |
| Fora da lista de 11/06 com movimentação na base | 0 |
| Fora da lista de 11/06 sem movimentação na base | 19 |
| Com movimentação e saldo líquido zero | 0 |

Todos os 334 municípios com movimentação na base estão na lista da Defesa
Civil. Os 144 restantes da lista são **casos para investigação de cobertura
da base detalhada do FUNDEC**, não uma lista de municípios sem assistência.
Até a data do extrato, 237 dos 478 já tinham alguma movimentação registrada;
a comparação com a base até setembro inclui mais 97 municípios com registro.

## Limites e próximos cruzamentos

- A lista é um retrato de 11/06/2024; a base FUNDEC vai até 26/09/2024.
- “Afetado” na lista da Defesa Civil não estabelece elegibilidade jurídica a
  esse fundo específico. O [Decreto nº 57.604/2024](https://www.defesacivil.rs.gov.br/legislacao-geral-de-defesa-civil)
  e os atos municipais precisam ser examinados antes de qualquer conclusão
  sobre elegibilidade individual.
- Ausência de linha nesta base não exclui repasses por outros programas,
  esferas, períodos ou modalidades de apoio.
- A lista não informa gravidade municipal nem total de pessoas atingidas;
  portanto, a análise não mede necessidade, suficiência ou equidade.
- Os 144 casos devem ser confrontados com publicações municipais, outros
  painéis de repasses e a atualização histórica da Defesa Civil antes de
  recomendações sobre atendimento.

## Roteiro da Tela 3 no Qlik Cloud

1. Envie `cobertura_municipal.csv` à conexão `DataFiles`, acrescente a seção
   correspondente de [`qlik/load_data.qvs`](../qlik/load_data.qvs) e recarregue.
   A única chave compartilhada com as tabelas atuais deve ser
   `chave_municipal`; confira que o modelo não criou chaves sintéticas. O
   arquivo deve ficar disponível em `DataFiles` sem ser adicionado também como
   tabela pelo Gerenciador de dados. Se isso ocorrer, remova apenas a tabela
   gerada pelo Gerenciador e mantenha a carga escrita no editor.
2. Crie a pasta **Tela 3 — Cobertura e lacunas (H4)**. Mostre KPIs para 478
   municípios listados, 334 listados com movimentação e 144 listados sem
   movimentação na base completa. Indique no subtítulo as datas das fontes.
3. Mostre um mapa ou tabela municipal com `localizacao_cobertura`,
   `municipio_cobertura`, `situacao_comparacao`, `qtd_movimentacoes_base` e
   `saldo_liquido_base`. Dê destaque à categoria `afetado_sem_registro`, sem
   chamá-la de “sem repasse” ou “não atendido”.
4. Inclua filtros para `situacao_comparacao` e `situacao_na_base`, além de uma
   nota com a fonte, a data do extrato e os limites acima. Valide alguns
   municípios de cada categoria contra os CSVs.
5. Exporte o aplicativo **com dados** em um novo snapshot sequencial após o 08,
   registre tamanho, SHA-256 e evidências, e reimporte para conferir a
   restauração.

## Conferência da Tela 3 e snapshot 09

O usuário informou em 17/09/2026 que carregou a cobertura, eliminou a carga
duplicada e conferiu o modelo sem `$Syn`, com `cobertura_municipal` associada
por `chave_municipal`. A seção `Normalização`, que restaura nomes de campos da
dimensão municipal, foi posicionada **depois** da seção gerada automaticamente:
`RENAME FIELD` precisa ser executado após a carga dos campos correspondentes.
Isso recuperou os gráficos da Tela 4 e o mapa de áreas da distribuição
geográfica. No mapa, a dimensão `localizacao_mapa` foi atribuída novamente à
camada de áreas.

Os três KPIs da Tela 3 mostraram **478**, **334** e **144** sem seleções. O
usuário informou que acrescentou a tabela municipal, os filtros, a nota de
limites e conferiu os controles solicitados. A expressão da medida mestra
**Municípios atendidos** na Visão Geral passou a ser
`Count(DISTINCT municipio_ibge_2024)`, preservando o recorte dos 334 municípios
com movimentação após a inclusão dos 497 municípios na cobertura.

O aplicativo exportado com dados foi colocado em
[`qlik/versoes-do-app/09-task-16/app.qvf`](../qlik/versoes-do-app/09-task-16/app.qvf).
O [README do snapshot](../qlik/versoes-do-app/09-task-16/README.md) registra
tamanho, SHA-256 e dependências de restauração. Os controles e limites da
evidência estão no [registro da Task 16](./evidencias/task-16/README.md).
As capturas atuais da Tela 3 e do modelo estão arquivadas nesse registro.
Em 18/09/2026, a tabela dinâmica foi substituída por uma tabela simples que
exibe código IBGE, classificações, movimentações e saldo em colunas. A captura
filtrada confirma **144 / 0 / 144** para `afetado_sem_registro`. A correção foi
exportada no [snapshot 10](../qlik/versoes-do-app/10-task-18/README.md), junto
com a Tela 5. A reimportação do QVF 10 ainda não foi confirmada.
