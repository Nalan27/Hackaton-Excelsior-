# Task 13 — Capa do App com Filtros e KPIs

## Objetivo

Criar a página inicial ("Visão Geral") do aplicativo Qlik Sense com filtros interativos e 4 KPIs em destaque, conforme solicitado na issue:

- **Total Repassado** — soma líquida de todos os repasses
- **Cidades Contempladas** — quantidade de municípios atendidos
- **Média por Pessoa** — valor líquido dividido pela população
- **Tempo Médio de Espera** — média de dias até o primeiro repasse

## Pré-requisitos

| Task | Descrição | Status |
|---|---|---|
| #10 | Calcular intervalo até o primeiro repasse | ✅ Concluída |
| #12 | Criar cálculos reutilizáveis | ✅ Concluída |

## Medidas Utilizadas

As 4 medidas foram criadas como **itens mestres** no Qlik Sense, conforme definido em [`qlik/medidas-mestras.md`](../qlik/medidas-mestras.md):

| KPI | Expressão Qlik | Valor sem filtros |
|---|---|---|
| **Total Repassado** | `Sum(valor)` | R$ 288.699.999,97 |
| **Cidades Contempladas** | `Count(DISTINCT chave_municipal)` | 334 |
| **Média por Pessoa** | `Sum(valor) / Sum(Aggr(Only(populacao_2024), chave_municipal))` | R$ 32,89 |
| **Tempo Médio de Espera** | `Avg({$<status_intervalo={"ok"}>} intervalo_desde_marco_adotado_dias)` | 40,13 dias |

## Filtros Implementados

Três filtros foram adicionados à página inicial para interatividade:

| Filtro | Campo | Origem |
|---|---|---|
| **Município** | `município` | `dim_municipio` |
| **Data** | `data` | `dim_calendario` / `fato_repasses` |
| **Recurso** | `recurso` | `fato_repasses` |

Todos os filtros atualizam os 4 KPIs de forma consistente com as master measures da Task #12.

## Layout da Página

```
┌─────────────────────────────────────┐
│  TÍTULO: Análise FUNDEC/RS           │
├─────────────────┬───────────────────┤
│  FILTROS:        │  KPI 1:           │
│  - Município     │  Total Repassado  │
│  - Data          │  R$ 288.699.999   │
│  - Recurso       │                   │
├─────────────────┼───────────────────┤
│                 │  KPI 2:           │
│                 │  Cidades: 334     │
├─────────────────┼───────────────────┤
│                 │  KPI 3:           │
│                 │  Média: R$ 32,89  │
├─────────────────┼───────────────────┤
│                 │  KPI 4:           │
│                 │  Espera: 40 dias  │
└─────────────────┴───────────────────┘
```

## Validação

### Testes Automatizados

Os 17 testes do `tests/test_etl_outputs.py` foram executados com sucesso, confirmando:

- ✅ Valores das medidas mestras sem filtros
- ✅ Seleção conjunta de municípios (Porto Alegre + Canoas)
- ✅ Preservação dos 18 valores negativos
- ✅ Integridade das associações no modelo de dados
- ✅ Script Qlik com sintaxe CSV válida

### Conferência Manual no Qlik Sense

| Cenário | Total Repassado | Cidades | Média Pessoa | Tempo Espera |
|---|---|---|---|---|
| Sem filtros | R$ 288.699.999,97 | 334 | R$ 32,89 | 40,13 dias |
| Porto Alegre | R$ 5.782.558,14 | 1 | R$ 4,16 | 84 dias |
| Porto Alegre + Canoas | R$ 11.565.116,28 | 2 | R$ 6,61 | — |
| Recurso Judiciário | R$ 180.000.000,00 | 95 | R$ 30,93 | 36,71 dias |

## Evidências

As capturas foram adicionadas em `docs/evidencias/task-13/`:

| Arquivo | Descrição | Status |
|---------|-----------|--------|
| `01-capa-geral.png` | Visão geral da página com os 4 KPIs | ✅ Concluído |
| `02-capa-filtros.png` | Município e data aplicados, com atualização dos KPIs | ✅ Concluído |
| `03-capa-selecao-multipla.png` | Seleção conjunta de sete municípios | ✅ Concluído |

![Capa geral](./evidencias/task-13/01-capa-geral.png)

![Filtros](./evidencias/task-13/02-capa-filtros.png)

![Seleção múltipla](./evidencias/task-13/03-capa-selecao-multipla.png)

### Limitações visuais registradas

As capturas confirmam a presença dos quatro KPIs, dos três filtros e a
atualização dos indicadores após as seleções. A revisão também identificou os
seguintes ajustes de apresentação para uma entrega posterior:

- ampliar os objetos para evitar títulos e valores truncados;
- padronizar a formatação monetária e decimal para `pt-BR`;
- exibir a unidade `dias` no indicador de tempo médio;
- identificar visualmente a fonte e o período analisado;
- registrar novas evidências para os cenários de Porto Alegre + Canoas e do
  recurso Judiciário.

Esses ajustes exigem uma nova edição no Qlik Sense e serão acompanhados em uma
issue de correção separada, com novo snapshot e novas evidências.

## Conclusão

A capa do app foi criada na página inicial do aplicativo Qlik Sense com:

- ✅ 4 KPIs em destaque (total repassado, cidades contempladas, média por pessoa, tempo médio de espera)
- ✅ 3 filtros interativos (município, data, recurso)
- ✅ Medidas consistentes com as master measures da Task #12
- ✅ Indicador de espera incluído (validado na Task #10)
- ✅ Todos os testes automatizados aprovados (17/17)
- ✅ Snapshot do aplicativo exportado com dados
- ✅ Evidências visuais documentadas
- ⚠️ Ajustes de apresentação registrados para acompanhamento

## Próximas Tasks Desbloqueadas

Com esta task concluída, as seguintes tasks podem ser iniciadas:

- **#19** — Montar Tela 6 (Resumo)
- **#20** — Testar usabilidade do App
- **#21** — Redigir o documento escrito
- **#22** — Gravar o pitch
- **#24** — Auditar o link público

## Estado

Implementação funcional concluída em 15/09/2026. A página inicial do aplicativo
Qlik Sense foi configurada com os quatro KPIs e os três filtros solicitados. Os
ajustes visuais identificados na revisão serão tratados em uma issue de correção
separada.
