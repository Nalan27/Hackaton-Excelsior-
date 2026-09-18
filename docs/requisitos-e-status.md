# Requisitos e status do projeto

## 1. Como ler este checklist

Este documento foi iniciado em **16 de setembro de 2026** e revisado em
**18 de setembro de 2026** após a conclusão da Task 19 ([PR #46](https://github.com/Nalan27/Hackaton-Excelsior-/pull/46)).
O estado de publicação e das entregas externas ainda precisa ser confirmado
antes da submissão.

- `[x]` significa que há evidência verificável no repositório.
- `[ ] Parcial` significa que existe um artefato inicial, mas ele ainda não atende ao requisito completo.
- `[ ] Pendente` significa que o requisito ainda precisa ser implementado.
- `[ ] Não comprovado` significa que depende de informação, conta, certificado ou ação externa que não está versionada no repositório.

Um arquivo existente não é considerado concluído se estiver vazio, inconsistente com a estrutura atual ou sem evidência de funcionamento.

### Prazos atualizados informados pela equipe

- Workshops: de **03/08 a 24/08/2026**.
- Cursos na Qlik: de **29/06 a 10/09/2026**, com conclusão até **10/09/2026**.
- Construção e entrega do desafio: de **01/09 a 20/09/2026**, com submissão até **20/09/2026**.

Esses períodos substituem as datas anteriores dessas etapas. O período atualizado de seleção interna e os horários-limite não foram informados; consulte o [cronograma](./edital-hackathon-qlik-2026.md#15-cronograma-do-evento) para as ressalvas.

## 2. Resumo do estado atual

| Área | Estado | Evidência principal |
|---|---|---|
| Dados brutos do FUNDEC | Concluído | 658 movimentações e ranking de 334 municípios em `data/raw/csv/` |
| Dados de população e indicadores socioeconômicos | Concluído | SIDRA 2024 e base municipal com código IBGE, PIB e IDH-M |
| Documentação do problema e dos requisitos | Concluído | Documentos desta pasta |
| Pipeline de tratamento reproduzível | Concluído | `etl/analis_de_dados.py` lê CSVs corretamente, trata tipos, preserva negativos e gera CSVs validados |
| Banco analítico validado | Parcial | CSVs validados em `data/processed/`; banco SQLite gerado mas `*.db` está no `.gitignore` |
| Aplicativo e dashboard Qlik Sense | Parcial para entrega | Telas 0 a 6 capturadas no [snapshot 11](../qlik/versoes-do-app/11-task-19/README.md), exportado com dados e reimportado segundo o usuário; acesso público e teste final de usabilidade pendentes |
| Análises e achados finais | Concluídos no app | A Tela 6 reúne quatro achados, recomendações e limites; falta consolidá-los e revisá-los no documento final |
| Documento descritivo final | Pendente | Há documentação de métodos e análises, mas não um relatório final consolidado e revisado ([issue #21](https://github.com/Nalan27/Hackaton-Excelsior-/issues/21)) |
| Vídeo pitch | Pendente | Não há roteiro, arquivo ou link |
| Certificados e elegibilidade da equipe | Parcial | Há 11 PDFs versionados para Alan, John-Victor e Martins-Sallys; faltam a conferência por integrante e a comprovação dos demais critérios ([issue #23](https://github.com/Nalan27/Hackaton-Excelsior-/issues/23)) |
| Publicação e envio | Pendente | Não há links públicos registrados nem comprovante de submissão ([issues #24](https://github.com/Nalan27/Hackaton-Excelsior-/issues/24) e [#25](https://github.com/Nalan27/Hackaton-Excelsior-/issues/25)) |

## 3. Requisitos eliminatórios

Todos os itens desta seção precisam estar concluídos. O atendimento parcial não habilita o trabalho para avaliação.

- [ ] **Pendente — Link público e funcional do aplicativo Qlik Sense.** Não há URL pública registrada.
- [x] **Visualização geográfica por município.** A Task 14 implementa mapa de pontos por valor líquido e mapa de áreas por valor por pessoa.
- [x] **Análise temporal dos repasses ou pagamentos.** A Task 15 apresenta créditos, ajustes e saldo líquido por mês.
- [x] **Pelo menos um KPI quantitativo.** Seis medidas mestras foram implementadas e validadas na pasta `Validação — Task 12` do aplicativo.
- [ ] **Pendente — Vídeo pitch público com até 5 minutos.** Não há vídeo nem link.
- [ ] **Parcial — Documento descritivo completo.** Contexto e bases constam em [`edital-hackathon-qlik-2026.md`](./edital-hackathon-qlik-2026.md); análises, achados e recomendações estão distribuídos nas Tasks 16 a 19. Falta o relatório final consolidado, com metodologia executada, conclusões, declaração de IA e revisão por outro integrante.
- [ ] **Parcial — Certificados das trilhas obrigatórias de todos os integrantes.** Há 11 PDFs em [`certificates/`](../certificates/), mas a lista final da equipe, os cursos exigidos e a conclusão por pessoa ainda não foram conferidos; a pasta de Henrique não contém PDF versionado.

## 4. Organização e conformidade do repositório

- [x] Trabalho realizado em branch própria: `feature/documentacao-edital-2026`.
- [x] `main` atualizada antes da criação da branch.
- [x] Documentação centralizada na pasta `docs/`.
- [x] Dados brutos separados em `data/raw/`.
- [x] Dependências Python registradas em `requirements.txt`.
- [x] Fontes públicas catalogadas em [`data/README.md`](../data/README.md).
- [x] Instruções de execução correspondem ao pipeline e aos artefatos gerados.
- [x] Validações críticas interrompem o ETL em caso de erro e são verificadas por testes automatizados.
- [ ] **Parcial — Definir política para artefatos do Qlik e arquivos gerados.** QVFs com dados, metadados e Git LFS estão documentados; falta definir publicação e retenção externas.

## 5. Aquisição e cobertura dos dados

- [x] Base detalhada de repasses do FUNDEC disponível: `repasses_fundec_2024.csv`.
- [x] Ranking oficial por município disponível: `ranking_oficial_fundec_2024.csv`.
- [x] População estimada dos 497 municípios do RS disponível: `populacao_rs_2024.csv`.
- [x] Base municipal complementar com código IBGE, PIB, área, densidade e IDH-M disponível: `municipios-brasil.csv`.
- [x] Documentos legais e de referência disponíveis em `data/raw/pdf/`.
- [x] Bases auxiliares de recursos recebidos e convênios disponíveis.
- [ ] **Pendente — Registrar data de extração, URL exata, filtros e versão junto a cada arquivo.** O catálogo contém fontes, mas não toda a linhagem necessária para reprodução.
- [ ] **Pendente — Obter indicador de impacto por município.** Selecionar uma medida comparável, como pessoas afetadas, danos estimados, população desalojada ou reconhecimento de calamidade.
- [x] **Adotar marco temporal documentado para os municípios atendidos.** Foi adotado 24/04/2024, início do período estadual dos eventos segundo o Decreto nº 57.604/2024. O marco é comum e não equivale à data do impacto local.

## 6. ETL e qualidade dos dados

- [x] Existe um script de ETL: [`etl/analis_de_dados.py`](../etl/analis_de_dados.py).
- [x] Leitura dos CSVs correta (caminhos, separadores e encoding consistentes).
- [x] Tipos de dados corrigidos: data como datetime, valor como decimal com sinal, cnpj/processo/empenho como string.
- [x] Estornos e ajustes preservados: 18 valores negativos mantidos no cálculo líquido.
- [x] Conciliação gerada em CSV: fato R$ 288.699.999,97 vs ranking R$ 289.176.004,25 (diferença R$ -476.004,28, concentrada em 3 municípios).
- [x] Chave municipal confiável criada via `municipios-brasil.csv` com normalização de acentos (334/334 municípios com código IBGE).
- [x] Duplicidades verificadas (0 duplicatas exatas encontradas).
- [x] Relatório de qualidade gerado: `data/processed/relatorio_validacao.csv`.
- [x] Arquivos tratados gerados de forma reproduzível (CSVs em `data/processed/` + SQLite na raiz).
- [x] Pipeline validado: execução bem-sucedida com 658 registros, 18 negativos, 0 chaves nulas.
- [x] Ausências nos indicadores documentadas: `idhm_2010` indisponível para Pinto Bandeira na fonte.

## 7. Modelo de dados e carga no Qlik Sense

- [x] **Implementar `fato_repasses` com valor numérico assinado.** Coluna `valor` como float com sinal, incluindo 18 estornos negativos.
- [x] **Implementar `dim_municipio` com código IBGE e atributos geográficos.** `chave_municipal`, `codigo_ibge`, `regiao`, `populacao_2025`, `densidade_hab_km2`, `area_km2`.
- [x] **Implementar dimensão socioeconômica com ano de referência explícito.** `idhm_2010`, `pib_per_capita_2023_reais`, `pib_2023_mil_reais`.
- [x] **Implementar calendário principal.** `dim_calendario.csv` possui 133 datas contínuas, com ano, trimestre, mês, nome do mês e ano-mês.
- [ ] **Pendente — Incorporar dimensão ou indicador de impacto, caso a fonte seja obtida.**
- [x] **Criar script de carga do Qlik compatível com os artefatos gerados.** Disponível em `qlik/load_data.qvs`.
- [x] **Evitar chaves sintéticas e associações circulares.** Modelo validado no Qlik sem chaves sintéticas ou associações circulares.
- [x] **Registrar fórmulas e regras das medidas mestres.** Catálogo reproduzível em `qlik/medidas-mestras.md`, com seis itens mestres validados no Qlik Cloud.
- [ ] **Pendente — Testar recarga completa e incremental, se aplicável.**

## 8. Análises exigidas e recomendadas

### 8.1 Distribuição geográfica

- [x] **Construir mapa municipal.** A Task 14 combina pontos dimensionados pelo valor líquido e áreas coloridas pelo valor por pessoa.
- [x] **Exibir valor total e valor per capita.** O ETL fornece total líquido e valor por pessoa com população IBGE 2024; o protótipo colore os pontos pelo indicador per capita.
- [ ] **Pendente — Identificar maiores e menores recebedores com contexto.**
- [ ] **Pendente — Comparar repasse com indicador de impacto.** Depende da fonte ainda não incorporada.

### 8.2 Tempo de repasse

- [x] **Construir timeline de créditos e estornos.** A Task 15 exibe créditos, ajustes negativos e saldo líquido entre maio e setembro de 2024.
- [x] **Calcular a data do primeiro repasse por município.** A menor data com `valor > 0` foi calculada para os 334 municípios; estornos não iniciam atendimento.
- [x] **Calcular dias desde o marco oficial adotado.** O artefato `intervalo_primeiro_repasse.csv` calcula o intervalo desde 24/04/2024 e explicita que a medida não representa tempo desde o impacto local.
- [ ] **Pendente — Identificar municípios atendidos sistematicamente mais tarde.**

### 8.3 Concentração, lacunas e equidade

- [x] **Calcular participação dos top 5, 10 e 20 municípios.** A [Task 17](./task-17-concentracao.md) registra 10,01%, 19,30% e 34,03% do saldo líquido, respectivamente.
- [ ] **Pendente — Comparar média, mediana, percentis e distribuição per capita.**
- [ ] **Parcial — Comparar municípios afetados com registros FUNDEC.** A Task 16 cruza os 478 nomes do extrato da Defesa Civil de 11/06/2024 com a base detalhada até 26/09/2024 e identifica 144 listados sem movimentação nessa base. A Tela 3 foi capturada no snapshot 11, reimportado segundo o usuário. Falta corroboração externa dos casos antes de recomendações sobre atendimento. Ausência de registro não demonstra ausência de atendimento.
- [ ] **Pendente — Definir critério reproduzível de subatendimento.**
- [ ] **Parcial — Analisar relação com IDH-M, PIB per capita, população e densidade.** A Task 18 concluiu a comparação descritiva entre IDH-M 2010 e valor líquido por habitante, com teste de sensibilidade por porte populacional. PIB per capita e densidade ainda não foram examinados nessa análise.
- [x] **Explicar limites e evitar interpretar correlação como causalidade.** A [Task 18](./task-18-vulnerabilidade-repasses.md) e a Tela 6 delimitam o universo de 333 municípios comparáveis, os anos das fontes e o caráter descritivo da associação com IDH-M.

## 9. Dashboard e experiência no Qlik Sense

- [x] **Concluído — Criar página de visão geral com KPIs e narrativa.** (Task 13)
- [x] **Concluído — Criar página geográfica.** (Task 14)
- [x] **Concluído — Criar página temporal.** (Task 15)
- [x] **Concluído — Criar página de cobertura e lacunas.** A Tela 3 cruza os 478 municípios listados pela Defesa Civil com as movimentações FUNDEC e identifica 144 sem registro nesta base. (Task 16)
- [x] **Concluído — Criar página de concentração.** A Tela 4 compara os maiores saldos, a participação no total e valores por pessoa. (Task 17)
- [x] **Concluído — Criar página de vulnerabilidade e repasses.** A Tela 5 da Task 18 mostra IDH-M 2010 × valor líquido por habitante, tabela municipal e nota metodológica; o usuário confirmou a reimportação dos snapshots 10 e 11.
- [x] **Concluído — Criar página final de resumo.** A Tela 6 reúne quatro achados validados, recomendações e limites; há [captura e QVF no snapshot 11](../qlik/versoes-do-app/11-task-19/README.md). (Task 19)
- [ ] **Parcial — Exibir método, limitações e recomendações no aplicativo.** A Tela 6 explicita recomendações e limites; a metodologia está distribuída entre telas e documentação, sem página própria de método.
- [x] **Concluído — Adicionar filtros úteis e consistentes entre páginas.** (Task 13)
- [ ] **Pendente — Implementar navegação e títulos dinâmicos.**
- [ ] **Parcial — Testar legibilidade, contraste, unidades, escalas e tooltips.** Há capturas das sete telas, mas falta a [revisão final de usabilidade](https://github.com/Nalan27/Hackaton-Excelsior-/issues/20) com filtros e estados sem dados.
- [ ] **Parcial — Exibir fonte, período e data de atualização.** Fontes e períodos aparecem nas notas de algumas telas; falta conferir cobertura uniforme e explicitar a data de atualização do aplicativo.
- [ ] **Pendente — Testar acesso público sem credenciais da equipe.**

## 10. Documento descritivo final

- [x] Contextualização do problema documentada.
- [x] Inventário das bases disponíveis documentado.
- [x] Metodologia planejada documentada.
- [ ] **Pendente — Consolidar no relatório a metodologia realmente executada.** As regras constam nas Tasks 12 e 16 a 18, mas ainda não formam um documento final único.
- [ ] **Pendente — Consolidar no relatório as análises e os achados com evidências.** A Tela 6 e o [snapshot 11](../qlik/versoes-do-app/11-task-19/README.md) registram quatro achados para revisão editorial.
- [ ] **Pendente — Inserir conclusões que respondam às perguntas do edital.**
- [ ] **Pendente — Consolidar no relatório as recomendações ligadas aos achados.** A Tela 6 já apresenta recomendações e limites, ainda não transpostos ao documento final.
- [ ] **Pendente — Declarar limitações, vieses, períodos e diferenças entre fontes.**
- [ ] **Pendente — Inserir declaração final de uso de IA com validação humana.** Há uma declaração preliminar na especificação.
- [ ] **Pendente — Revisar texto, números e referências por pelo menos outro integrante.**

## 11. Vídeo pitch

- [ ] **Pendente — Criar roteiro com problema, método, insights, diferenciais, conclusões e recomendações.**
- [ ] **Pendente — Selecionar apenas visualizações essenciais para a narrativa.**
- [ ] **Pendente — Gravar e editar o vídeo.**
- [ ] **Pendente — Garantir duração máxima de 5 minutos.**
- [ ] **Pendente — Publicar com link público.**
- [ ] **Pendente — Testar áudio, imagem, legenda e acesso em janela anônima.**

## 12. Equipe, inscrição e trilhas

- [ ] **Não comprovado — Equipe inscrita no prazo.**
- [ ] **Não comprovado — Equipe formada por 3 a 5 integrantes elegíveis.**
- [ ] **Não comprovado — Todos os integrantes estão regularmente matriculados e ativos em curso aceito.**
- [ ] **Não comprovado — Nenhum integrante é colaborador da Unicesumar.**
- [ ] **Parcial — Trilhas obrigatórias concluídas por todos até 10/09/2026.** Há 11 PDFs versionados para três pessoas; falta conferir a lista final de integrantes, cursos e datas de conclusão. A pasta de Henrique não contém PDF versionado.
- [ ] **Parcial — Certificados reunidos e legíveis.** Há PDFs em `certificates/`, mas a conferência de nomes, cursos, legibilidade e acesso pelo responsável pelo envio não foi registrada.
- [ ] **Não comprovado — Representante responsável pela submissão definido.**

## 13. Originalidade, ética e uso de IA

- [x] Uso do OpenAI Codex nesta etapa registrado na documentação.
- [ ] **Pendente — Revisar e complementar a declaração com todas as ferramentas de IA usadas pela equipe.**
- [ ] **Pendente — Registrar finalidade, etapas e validação humana de cada uso.**
- [ ] **Pendente — Verificar autoria e licenças de dados, imagens, ícones, músicas e demais materiais.**
- [ ] **Pendente — Validar manualmente todos os cálculos, textos e insights assistidos por IA.**
- [ ] **Pendente — Preparar a equipe para explicar e defender a metodologia sem depender de conteúdo gerado.**

## 14. Publicação e submissão

- [ ] **Pendente — Publicar o aplicativo Qlik Sense e registrar o link.**
- [ ] **Pendente — Publicar o vídeo e registrar o link.**
- [ ] **Pendente — Finalizar e publicar o documento descritivo.**
- [ ] **Pendente — Reunir os certificados de todos os integrantes.**
- [ ] **Pendente — Testar todos os links fora das contas da equipe.**
- [ ] **Pendente — Confirmar que os links permanecerão ativos até o encerramento oficial.**
- [ ] **Pendente — Conferir pesos da rubrica no edital original.** O PDF fornecido não permitiu leitura confiável de toda a coluna.
- [ ] **Pendente — Realizar revisão eliminatória independente antes do envio.**
- [ ] **Pendente — Fazer uma única submissão pelo representante até 20/09/2026, dentro do período de construção e entrega de 01/09 a 20/09/2026.**

## 15. Ordem de execução recomendada

### Prioridade 0 — Evitar desclassificação

1. Conferir equipe, trilhas, certificados e responsável pela submissão ([issue #23](https://github.com/Nalan27/Hackaton-Excelsior-/issues/23)).
2. Finalizar e revisar o documento descritivo e o vídeo de até 5 minutos ([issues #21](https://github.com/Nalan27/Hackaton-Excelsior-/issues/21) e [#22](https://github.com/Nalan27/Hackaton-Excelsior-/issues/22)).
3. Testar usabilidade, publicar e auditar os links do aplicativo, documento e vídeo fora das contas da equipe ([issues #20](https://github.com/Nalan27/Hackaton-Excelsior-/issues/20) e [#24](https://github.com/Nalan27/Hackaton-Excelsior-/issues/24)).
4. Fazer uma única submissão completa e guardar o comprovante até 20/09/2026 ([issue #25](https://github.com/Nalan27/Hackaton-Excelsior-/issues/25)).

### Prioridade 1 — Garantir consistência analítica

1. Conferir os números e conclusões do documento final contra os CSVs validados e as Telas 0 a 6.
2. Preservar no documento o tratamento dos 18 lançamentos negativos e a diferença de R$ 476.004,28 entre fato e ranking.
3. Explicitar os universos, anos e limites dos indicadores; não interpretar correlação ou ausência de registro como causalidade ou falta de atendimento.
4. Registrar a causa do ajuste negativo de julho, se for confirmada por fonte verificável; até lá, manter sua causa como desconhecida.

### Prioridade 2 — Buscar pontuação bônus

1. Incorporar indicador de impacto e marco temporal confiáveis.
2. Calcular métricas per capita e comparações normalizadas.
3. Cruzar repasses com vulnerabilidade socioeconômica.
4. Identificar desigualdades e lacunas por critério reproduzível.
5. Destacar insights originais e aplicáveis à tomada de decisão.

## 16. Critério para marcar este checklist como concluído

Um item só deve receber `[x]` quando houver evidência revisável: arquivo funcional, cálculo reproduzível, captura ou link testado, certificado ou registro de validação. Alegações sem evidência devem permanecer como pendentes ou não comprovadas.
