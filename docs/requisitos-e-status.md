# Requisitos e status do projeto

## 1. Como ler este checklist

Este documento foi iniciado em **16 de setembro de 2026** e revisado em
**22 de setembro de 2026** após o [comunicado de atualização da entrega](./atualizacao-submissao-2026-09-18.md).
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
- Prazo final de submissão do projeto: **23/09/2026**, prorrogado pela organização em comunicado recebido em 18/09/2026.

O comunicado não informou horário-limite nem novo período de seleção interna. As demais datas acima permanecem como referência anterior; consulte o [cronograma](./edital-hackathon-qlik-2026.md#15-cronograma-do-evento) e a [atualização de entrega](./atualizacao-submissao-2026-09-18.md).

## 2. Resumo do estado atual

| Área | Estado | Evidência principal |
|---|---|---|
| Dados brutos do FUNDEC | Concluído | 658 movimentações e ranking de 334 municípios em `data/raw/csv/` |
| Dados de população e indicadores socioeconômicos | Concluído | SIDRA 2024 e base municipal com código IBGE, PIB e IDH-M |
| Documentação do problema e dos requisitos | Concluído | Documentos desta pasta |
| Pipeline de tratamento reproduzível | Concluído | `etl/analis_de_dados.py` lê CSVs corretamente, trata tipos, preserva negativos e gera CSVs validados |
| Banco analítico validado | Parcial | CSVs validados em `data/processed/`; banco SQLite gerado mas `*.db` está no `.gitignore` |
| Aplicativo e dashboard Qlik Sense | Concluído no repositório | Telas 0 a 6 capturadas e validadas no [snapshot 12](../qlik/versoes-do-app/12-task-20/README.md); resta gravar a navegação do pitch. Link público do Qlik Sense foi dispensado |
| Análises e achados finais | Concluídos no app e consolidados no relatório | A Tela 6 reúne quatro achados, recomendações e limites; o relatório final os vincula às bases, cálculos e evidências |
| Documento descritivo final | Consolidado para revisão | [Relatório](relatorio-final.md) com capturas e explicação dos gráficos; a issue #21 foi concluída, mas ainda faltam revisão por segundo integrante e conferência da cópia no Drive |
| Vídeo pitch | Pendente | Não há roteiro ou arquivo; deve ter até cinco minutos, mostrar navegação pelo dashboard, apresentador visível e nenhuma narração por IA |
| Certificados e elegibilidade da equipe | Parcial | A equipe remanescente tem Alan, John-Victor e Martins-Sallys; Henrique saiu em 12/09/2026. Há 11 PDFs em `certificates/` para os três integrantes, ainda sem conferência final ([issue #23](https://github.com/Nalan27/Hackaton-Excelsior-/issues/23)) |
| Publicação e envio | Pendente | Não há evidência registrada da auditoria da pasta pública do Drive nem comprovante de submissão pela Central Hackathon ([issues #24](https://github.com/Nalan27/Hackaton-Excelsior-/issues/24) e [#25](https://github.com/Nalan27/Hackaton-Excelsior-/issues/25)) |

## 3. Requisitos eliminatórios

A [orientação atualizada](./atualizacao-submissao-2026-09-18.md) substitui os
requisitos antigos de publicação do Qlik e de vídeos individuais das trilhas.
A entrega externa só estará pronta quando os itens aplicáveis forem conferidos.

- [ ] **Pendente — Pasta pública no Google Drive.** Usar o nome oficial da equipe, colocar todos os documentos na pasta e configurar “Qualquer pessoa com o link — Leitor”.
- [x] **Visualização geográfica por município.** A Tela 1 tem dois mapas e sua captura está no [relatório](./relatorio-final.md#47-capturas-do-dashboard-e-explicação-dos-gráficos).
- [x] **Análise temporal dos repasses ou pagamentos.** A Tela 2 apresenta créditos, ajustes e saldo líquido por mês; a captura está no relatório.
- [x] **Pelo menos um KPI quantitativo.** A Tela 0 e a Tela 6 exibem KPIs; suas capturas estão no relatório.
- [ ] **Pendente — Vídeo pitch de até cinco minutos.** Deve navegar pelo dashboard, mostrar quem apresenta e não ter narração por IA.
- [ ] **Parcial — Documento de texto no Drive.** O [relatório](./relatorio-final.md) contém contexto, bases, capturas, explicação dos gráficos, metodologia, achados, conclusões e recomendações; falta revisar e conferir a cópia com imagens legíveis no Drive.
- [ ] **A confirmar — Certificados das trilhas.** O comunicado dispensou vídeos individuais, mas não declarou dispensa dos certificados; organizar os PDFs e confirmar se precisam acompanhar o envio.

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
- [ ] **Parcial — Comparar municípios afetados com registros FUNDEC.** A Task 16 cruza os 478 nomes do extrato da Defesa Civil de 11/06/2024 com a base detalhada até 26/09/2024 e identifica 144 listados sem movimentação nessa base. A Tela 3 foi validada no snapshot 12, reimportado e testado. Falta corroboração externa dos casos antes de recomendações sobre atendimento. Ausência de registro não demonstra ausência de atendimento.
- [ ] **Pendente — Definir critério reproduzível de subatendimento.**
- [ ] **Parcial — Analisar relação com IDH-M, PIB per capita, população e densidade.** A Task 18 concluiu a comparação descritiva entre IDH-M 2010 e valor líquido por habitante, com teste de sensibilidade por porte populacional. PIB per capita e densidade ainda não foram examinados nessa análise.
- [x] **Explicar limites e evitar interpretar correlação como causalidade.** A [Task 18](./task-18-vulnerabilidade-repasses.md) e a Tela 6 delimitam o universo de 333 municípios comparáveis, os anos das fontes e o caráter descritivo da associação com IDH-M.

## 9. Dashboard e experiência no Qlik Sense

- [x] **Concluído — Criar página de visão geral com KPIs e narrativa.** (Task 13)
- [x] **Concluído — Criar página geográfica.** (Task 14)
- [x] **Concluído — Criar página temporal.** (Task 15)
- [x] **Concluído — Criar página de cobertura e lacunas.** A Tela 3 cruza os 478 municípios listados pela Defesa Civil com as movimentações FUNDEC e identifica 144 sem registro nesta base. (Task 16)
- [x] **Concluído — Criar página de concentração.** A Tela 4 compara os maiores saldos, a participação no total e valores por pessoa. (Task 17)
- [x] **Concluído — Criar página de vulnerabilidade e repasses.** A Tela 5 da Task 18 mostra IDH-M 2010 × valor líquido por habitante, tabela municipal e nota metodológica; a versão final está no snapshot 12, reimportado e testado.
- [x] **Concluído — Criar página final de resumo.** A Tela 6 reúne quatro achados validados, recomendações e limites; há [captura e QVF no snapshot 12](../qlik/versoes-do-app/12-task-20/README.md). (Tasks 19 e 20)
- [ ] **Parcial — Exibir método, limitações e recomendações no aplicativo.** A Tela 6 explicita recomendações e limites; a metodologia está distribuída entre telas e documentação, sem página própria de método.
- [x] **Concluído — Adicionar filtros úteis e consistentes entre páginas.** (Task 13)
- [ ] **Pendente — Implementar navegação e títulos dinâmicos.**
- [x] **Concluído — Testar legibilidade, contraste, unidades, escalas e tooltips.** A [revisão final de usabilidade](https://github.com/Nalan27/Hackaton-Excelsior-/issues/20) percorreu as sete telas com filtros, estados sem dados e casos de controle; as evidências estão no snapshot 12.
- [ ] **Parcial — Exibir fonte, período e data de atualização.** Fontes e períodos aparecem nas notas de algumas telas; falta conferir cobertura uniforme e explicitar a data de atualização do aplicativo.
- [ ] **Pendente — Testar a navegação do dashboard que será gravada no vídeo pitch.**

## 10. Documento descritivo final

- [x] Contextualização do problema documentada.
- [x] Inventário das bases disponíveis documentado.
- [x] Metodologia planejada documentada.
- [x] **Concluído para revisão — Consolidar no relatório a metodologia realmente executada.** Ver [`docs/relatorio-final.md`](relatorio-final.md).
- [x] **Concluído para revisão — Consolidar no relatório as análises e os achados com evidências.** As capturas das Telas 0 a 6 e a explicação dos gráficos estão no relatório, junto aos CSVs processados.
- [x] **Concluído para revisão — Inserir conclusões que respondam às perguntas do edital.**
- [x] **Concluído para revisão — Consolidar no relatório as recomendações ligadas aos achados.**
- [x] **Concluído para revisão — Declarar limitações, vieses, períodos e diferenças entre fontes.**
- [x] **Concluído para revisão — Inserir declaração final de uso de IA com validação humana.** A revisão final por outro integrante ainda precisa ser registrada.
- [x] **Capturas do dashboard e descrição de cada gráfico incluídas no relatório.**
- [ ] **Pendente — Revisar texto, números, capturas e referências por pelo menos outro integrante.**
- [ ] **Pendente — Conferir a cópia do documento no Drive, inclusive imagens e legibilidade.**

## 11. Vídeo pitch

- [ ] **Pendente — Criar roteiro com problema, método, insights, diferenciais, conclusões e recomendações.**
- [ ] **Pendente — Selecionar apenas visualizações essenciais para a narrativa.**
- [ ] **Pendente — Gravar navegação pelo dashboard e editar o vídeo.**
- [ ] **Pendente — Garantir duração máxima de 5 minutos.**
- [ ] **Pendente — Mostrar no vídeo quem apresentar; não usar narração por IA.** Nem todos os integrantes precisam apresentar.
- [ ] **Pendente — Colocar o vídeo na pasta pública do Drive.**
- [ ] **Pendente — Testar áudio, imagem e reprodução fora da conta da equipe.**

## 12. Equipe, inscrição e trilhas

- [ ] **Não comprovado — Equipe inscrita no prazo.**
- [ ] **Parcial — Equipe com três integrantes após saída de Henrique em 12/09/2026.** Alan, John-Victor e Martins-Sallys permanecem; confirmar elegibilidade e inscrição final.
- [ ] **Não comprovado — Todos os integrantes estão regularmente matriculados e ativos em curso aceito.**
- [ ] **Não comprovado — Nenhum integrante é colaborador da Unicesumar.**
- [ ] **Parcial — Trilhas obrigatórias concluídas pela equipe remanescente até 10/09/2026.** Há 11 PDFs versionados para Alan, John-Victor e Martins-Sallys; falta conferir cursos, nomes e datas de conclusão.
- [ ] **Parcial — Certificados reunidos e legíveis.** Há PDFs em `certificates/`, mas a conferência de nomes, cursos e legibilidade não foi registrada. O comunicado dispensa vídeos individuais, não afirma dispensa dos certificados.
- [ ] **Não comprovado — Representante responsável pela submissão definido.**

## 13. Originalidade, ética e uso de IA

- [x] Uso do OpenAI Codex nesta etapa registrado na documentação.
- [ ] **Pendente — Revisar e complementar a declaração com todas as ferramentas de IA usadas pela equipe.**
- [ ] **Pendente — Registrar finalidade, etapas e validação humana de cada uso.**
- [ ] **Pendente — Verificar autoria e licenças de dados, imagens, ícones, músicas e demais materiais.**
- [ ] **Pendente — Validar manualmente todos os cálculos, textos e insights assistidos por IA.**
- [ ] **Pendente — Preparar a equipe para explicar e defender a metodologia sem depender de conteúdo gerado.**

## 14. Publicação e submissão

- [ ] **Pendente — Criar pasta no Google Drive com o nome oficial da equipe e acesso público como Leitor.**
- [ ] **Pendente — Colocar documento de texto e vídeo pitch na mesma pasta.**
- [ ] **Pendente — Conferir prints, descrições, áudio e vídeo fora das contas da equipe.**
- [ ] **A confirmar — Verificar com a organização se os certificados também devem acompanhar a pasta.** Vídeos individuais não são exigidos.
- [ ] **Pendente — Conferir pesos da rubrica no edital original.** O PDF fornecido não permitiu leitura confiável de toda a coluna.
- [ ] **Pendente — Realizar revisão independente antes do envio.**
- [ ] **Pendente — Definir o único integrante que enviará pela [Central Hackathon](https://fabioacs.github.io/painel-hackathon).** Somente quem enviou pode atualizar o projeto.
- [ ] **Pendente — Fazer a submissão até 23/09/2026 e guardar o comprovante.**

## 15. Ordem de execução recomendada

### Prioridade 0 — Evitar desclassificação

1. Conferir equipe, trilhas, certificados e responsável pela submissão ([issue #23](https://github.com/Nalan27/Hackaton-Excelsior-/issues/23)).
2. Revisar o relatório, levar o documento com prints ao Drive e gravar o pitch de até cinco minutos com navegação pelo dashboard ([issues #21](https://github.com/Nalan27/Hackaton-Excelsior-/issues/21) e [#22](https://github.com/Nalan27/Hackaton-Excelsior-/issues/22)).
3. Auditar o acesso de leitor à pasta, ao documento e ao vídeo fora das contas da equipe ([issue #24](https://github.com/Nalan27/Hackaton-Excelsior-/issues/24)); a revisão de usabilidade do dashboard foi concluída na issue #20.
4. Fazer uma única submissão completa pela Central Hackathon e guardar o comprovante até 23/09/2026 ([issue #25](https://github.com/Nalan27/Hackaton-Excelsior-/issues/25)).

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
