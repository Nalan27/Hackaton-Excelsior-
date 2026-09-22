# Monitoramento e Raspagem de Dados - FUNDEC / Reconstrução RS

Este repositório destina-se ao rastreamento, mapeamento e raspagem de dados públicos sobre o **FUNDEC (Fundo de Defesa Civil do Estado do Rio Grande do Sul)** e iniciativas de transparência e reconstrução do Estado decorrentes da calamidade pública de 2024.

---

## Status das Fontes de Dados

### 🟢 Dados Baixados (Coletados)

Os dados das seguintes fontes foram extraídos e organizados para análise:

| Fonte / Painel | Descrição / Conteúdo | Link de Origem |
| :--- | :--- | :--- |
| **Painel TCE-RS (Reconstrução RS)** | Dados estruturados do Tribunal de Contas do Estado sobre os recursos e ações de reconstrução. | [Acessar Painel](https://paineis.tcers.tc.br/extensions/ReconstrucaoRS/fundec.html) |
| **Portal da Transparência RS** | Dados temáticos das movimentações e transferências do FUNDEC (Calamidade Pública 2024). | [Acessar Transparência RS](https://www.transparencia.rs.gov.br/calamidade-publica-2024/1-2-tematico-fundo-de-defesa-civil-fundec/dados/) |
| **Lei Complementar nº 16.263/2024** | Institui a PEPDEC/SIEPDEC; revoga a Lei 13.599/2010 (criação do FUNDEC). | [Acessar](https://www.defesacivil.rs.gov.br/legislacao-geral-de-defesa-civil) |
| **Decreto (= materia1351760.pdf)** | Regulamenta o SIEPDEC e procedimentos de declaração de emergência/calamidade. | [Acessar](https://www.defesacivil.rs.gov.br/legislacao-geral-de-defesa-civil) |
| **Decreto nº 57.604/2024** | Critérios excepcionais de transferência de recursos do FUNDEC/RS aos municípios em calamidade — base legal direta dos repasses de 2024. | [Acessar](https://leisestaduais.com.br/rs/decreto-n-57604-2024-rio-grande-do-sul-dispoe-sobre-criterios-excepcionais-para-transferencia-de-recursos-no-fundo-estadual-de-defesa-civil-do-estado-do-rio-grande-do-sul-fundec-rs-aos-municipios-em-estado-de-calamidade-publica-ou-em-situacao-de-emergencia-decorrente-dos-eventos-climaticos-de-chuvas-intensas-no-territorio-do-estado-do-rio-grande-do-sul-de-que-trata-o-decreto-no-57-596-de-1-o-de-maio-de-2024) |
| **PLE 27/2024 (Três Forquilhas)** | Projeto de lei de crédito suplementar de R$200 mil com repasse extraordinário do FUNDEC. | [Acessar](https://camaratresforquilhas.rs.gov.br/wp-content/uploads/2024/08/PLE_27_2024.pdf) |
| **Recursos Recebidos (Portal da Transparência)** | Recursos recebidos pelo favorecido vinculado ao FUNDEC (fonte do recurso, não destino). | [Acessar](https://portaldatransparencia.gov.br/despesas/favorecido?faseDespesa=3&favorecido=319734&ordenarPor=valor&direcao=desc) |
| **Convênios e outros acordos firmados** | Convênios firmados pelo mesmo favorecido. | [Acessar](https://portaldatransparencia.gov.br/convenios/consulta?convenente=319734) |
| **Atlas Cidade — Dados Municipais** | Base compilada com IDH-M (2010), população, PIB e código IBGE dos municípios brasileiros. | [Acessar](https://www.atlascidade.com.br/dados) |
| **Defesa Civil do RS — Municípios Afetados** | Extrato nominal gerado em 11/06/2024 às 10:06, com 478 municípios afetados; não é lista de elegibilidade ao FUNDEC. | [PDF oficial](https://estado.rs.gov.br/upload/arquivos/202407/municipios-afetados-defesa-civil-8-7-2024.pdf) |
| **repasses_fundec_2024.csv** | 658 transferências individuais do FUNDEC (Calamidade Pública 2024) — base operacional da tabela fato. | [Portal da Transparência RS](https://www.transparencia.rs.gov.br/calamidade-publica-2024/1-2-tematico-fundo-de-defesa-civil-fundec/dados/) |
| **ranking_oficial_fundec_2024.csv** | Ranking oficial dos 334 municípios por valor total pago — referência para conciliação. | [Portal da Transparência RS](https://www.transparencia.rs.gov.br/calamidade-publica-2024/1-2-tematico-fundo-de-defesa-civil-fundec/dados/) |

O art. 1º do Decreto nº 57.604/2024 registra 24/04/2024 como início do
período estadual dos eventos climáticos. A task 10 usa essa data somente como
marco documental comum dos repasses, sem tratá-la como data do impacto local.

A Task 16 preserva o extrato da Defesa Civil em
`data/raw/pdf/defesa-civil-rs-municipios-afetados-2024-06-11.pdf` e gera em
`data/processed/` a lista conciliada por código IBGE, a tabela de cobertura
municipal, os casos para investigação e um relatório de controle. Consulte
[`docs/task-16-cobertura-lacunas.md`](../docs/task-16-cobertura-lacunas.md)
para o período, os critérios e as limitações do cruzamento.
        
### Arquivo de dados

O arquivo de população utilizado no projeto é:

`data/raw/csv/populacao_rs_2024.csv`

**Fonte:** IBGE — Sistema IBGE de Recuperação Automática (SIDRA), Tabela 6579.

[Consultar dados no SIDRA](https://sidra.ibge.gov.br/tabela/6579)

O arquivo de IDH-M, população e PIB utilizado no projeto é:

`data/raw/csv/municipios-brasil.csv`

**Fonte primária do IDH-M:** PNUD / Ipea / Fundação João Pinheiro — Atlas do Desenvolvimento Humano no Brasil (Censo 2010).
**Compilação:** Atlas Cidade.

[Consultar Atlas Brasil (fonte original)](https://www.atlasbrasil.org.br/) · [Baixar via Atlas Cidade](https://www.atlascidade.com.br/dados)

---
