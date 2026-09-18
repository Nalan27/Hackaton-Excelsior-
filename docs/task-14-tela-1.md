# Task 14 — Tela 1: Distribuição Geográfica

## Objetivo

Construir no Qlik Cloud uma página geográfica do Rio Grande do Sul que permita
comparar, entre os 334 municípios com movimentações registradas na base
detalhada do FUNDEC/RS, o valor líquido recebido e o valor líquido recebido por
pessoa.

A comparação por pessoa usa a população estimada pelo IBGE/SIDRA para 2024. O
indicador não mede população afetada, intensidade do impacto, necessidade ou
adequação do repasse.

## Dependências e escopo

- A Task 11 validou `localizacao_mapa` e o protótipo com os 334 municípios
  recebedores.
- A Task 12 definiu as medidas mestras reutilizadas nos mapas.
- A Task 13 estabeleceu o padrão de filtros e apresentação do aplicativo.
- A Task 15, já presente no aplicativo, corresponde ao snapshot 06. A
  exportação desta task é o snapshot 07.

O universo exibido não representa todos os 497 municípios do Rio Grande do Sul
nem um cadastro completo de municípios atingidos pelas enchentes.

## Medidas reutilizadas

| Indicador | Expressão Qlik | Unidade | Uso na tela |
|---|---|---|---|
| Valor líquido recebido | `Sum(valor)` | R$ | Tamanho das bolhas no mapa de pontos |
| Valor líquido recebido por pessoa | `If(Sum(Aggr(Only(populacao_2024), chave_municipal)) > 0, Sum(valor) / Sum(Aggr(Only(populacao_2024), chave_municipal)))` | R$/pessoa | Cor das áreas municipais |

As regras completas estão em
[`qlik/medidas-mestras.md`](../qlik/medidas-mestras.md). O valor líquido preserva
créditos e ajustes negativos. A população é agregada uma única vez por
município.

## Configuração da tela

### Filtros

| Título | Campo |
|---|---|
| Recurso | `recurso` |
| Mês | `mes_nome` |
| Município | `município` |

Os três filtros atuam sobre os dois mapas por meio do modelo associativo do
Qlik.

### Mapa de valor líquido recebido

- camada de pontos localizada por `localizacao_mapa`;
- tamanho das bolhas definido pela medida **Valor líquido recebido**;
- cor fixa para não codificar a mesma medida simultaneamente por cor e tamanho;
- título **Valor líquido recebido — FUNDEC/RS 2024**.

### Mapa de valor líquido recebido por pessoa

- camada de áreas municipais localizada por `localizacao_mapa`;
- cor definida pela medida **Valor líquido recebido por pessoa**;
- unidade apresentada como R$/pessoa;
- título **Valor líquido recebido por pessoa — FUNDEC/RS 2024**.

### Tooltips

Os dois mapas apresentam tooltip personalizado com:

- município;
- código IBGE;
- valor líquido da seleção atual;
- população estimada de 2024;
- valor líquido por pessoa da seleção atual.

As medidas dos tooltips são dinâmicas. Elas não usam os campos estáticos
`total_repasses` ou `valor_por_pessoa_2024`, pois esses campos representam o
período completo e não responderiam corretamente aos filtros de mês e recurso.

## Validação reproduzível

| Cenário | Resultado esperado e conferido |
|---|---|
| Sem seleções | Os mapas exibem os municípios recebedores no Rio Grande do Sul e usam legendas distintas para valor líquido e valor por pessoa. |
| Mês = Julho | Os dois mapas respondem à seleção e exibem somente municípios associados às movimentações de julho. |
| Município = Porto Alegre | O ponto e a área municipal são isolados; valor líquido de R$ 5.782.558,14 e valor por pessoa de R$ 4,16. |
| Tooltip de Porto Alegre | Código IBGE 4314902, população 1.389.322, valor líquido de R$ 5.782.558,14 e R$ 4,16 por pessoa. |
| Recurso = Judiciário | O filtro atualiza simultaneamente as duas visualizações. |

A validação da fonte confirma 334 chaves municipais, 334 localizações distintas,
população positiva para todos os recebedores e ausência de chaves órfãs na
tabela fato. A inspeção visual no Qlik não identificou geometrias fora do Rio
Grande do Sul.

## Evidências visuais

As capturas e seus estados de seleção estão catalogados em
[`docs/evidencias/task-14/README.md`](./evidencias/task-14/README.md):

1. `01-distribuicao-geografica-geral.png`;
2. `02-distribuicao-geografica-filtro-mes.png`;
3. `03-distribuicao-geografica-filtro-municipio.png`;
4. `04-tooltip-valor-total.png`;
5. `05-tooltip-valor-por-pessoa.png`;
6. `06-distribuicao-geografica-filtro-recurso.png`.

## Limitações

- A tela descreve valores recebidos e população, mas não mede diretamente
  impacto, necessidade, efetividade ou equidade.
- Os mapas cobrem municípios com movimentações na base analisada, não todo o
  universo de municípios atingidos.
- Os limites e pontos dependem da resolução geográfica do Qlik para
  `localizacao_mapa`.
- Diferenças de valor por pessoa não demonstram, isoladamente, distribuição
  justa ou injusta dos recursos.

## Snapshot 07

O aplicativo foi exportado com dados em
[`qlik/versoes-do-app/07-task-14/app.qvf`](../qlik/versoes-do-app/07-task-14/app.qvf).
Os metadados e as dependências estão no
[`README do snapshot`](../qlik/versoes-do-app/07-task-14/README.md).

## Estado

Implementada e validada em 16/09/2026. A reimportação do snapshot 07 e a
conferência do aplicativo foram confirmadas em 17/09/2026 e registradas nas
evidências da Task 14.
