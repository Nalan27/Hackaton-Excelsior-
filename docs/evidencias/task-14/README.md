# Evidências da Task 14 — Tela 1 (Distribuição Geográfica)

**Estado:** capturas do Qlik Cloud registradas e valores de controle conferidos
com a base processada.

## Capturas

| Arquivo | Estado da seleção | O que comprova |
|---|---|---|
| [`01-distribuicao-geografica-geral.png`](01-distribuicao-geografica-geral.png) | Sem filtros | Estrutura final da página, três filtros, mapa de pontos e mapa de áreas. |
| [`02-distribuicao-geografica-filtro-mes.png`](02-distribuicao-geografica-filtro-mes.png) | `mes_nome = Julho` | Atualização simultânea dos dois mapas pelo filtro mensal. |
| [`03-distribuicao-geografica-filtro-municipio.png`](03-distribuicao-geografica-filtro-municipio.png) | `município = Porto Alegre` | Isolamento do ponto e da área municipal. |
| [`04-tooltip-valor-total.png`](04-tooltip-valor-total.png) | Tooltip de Porto Alegre | Código IBGE, valor líquido, população e valor por pessoa no mapa de pontos. |
| [`05-tooltip-valor-por-pessoa.png`](05-tooltip-valor-por-pessoa.png) | Tooltip de Triunfo | Código IBGE, valor líquido, população e valor por pessoa na camada de áreas. |
| [`06-distribuicao-geografica-filtro-recurso.png`](06-distribuicao-geografica-filtro-recurso.png) | `recurso = Judiciário` | Resposta dos dois mapas ao filtro de fonte do recurso. |

## Valores de referência

| Controle | Valor |
|---|---:|
| Municípios recebedores | 334 |
| Valor líquido total | R$ 288.699.999,97 |
| Porto Alegre — código IBGE | 4314902 |
| Porto Alegre — população 2024 | 1.389.322 |
| Porto Alegre — valor líquido | R$ 5.782.558,14 |
| Porto Alegre — valor por pessoa | R$ 4,16 |

## Cobertura geográfica

A camada tratada contém 334 chaves municipais e 334 valores distintos de
`localizacao_mapa`. Todos os municípios recebedores possuem população positiva
e chave presente na tabela fato. A inspeção visual das camadas no Qlik não
identificou ponto ou área fora do Rio Grande do Sul.

## Conferência final

- [x] Mapa de pontos com tamanho pelo valor líquido.
- [x] Mapa de áreas com cor pelo valor por pessoa.
- [x] Filtros de recurso, mês e município aplicados aos dois mapas.
- [x] Tooltips com valores exatos e código IBGE.
- [x] Valores de Porto Alegre conciliados com a base processada.
- [ ] QVF final importado novamente em ambiente independente.

## Documentação relacionada

- [Documentação da Task 14](../../task-14-tela-1.md)
- [README do snapshot 07](../../../qlik/versoes-do-app/07-task-14/README.md)
