# Requisitos e status do projeto

## 1. Como ler este checklist

Este documento foi iniciado em **16 de setembro de 2026**, com atualização
pontual das Tasks 16 e 18 em **18 de setembro de 2026**. Os demais itens ainda
precisam de uma revisão geral antes da submissão.

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
| Aplicativo e dashboard Qlik Sense | Parcial | Visão geral e Telas 3 a 5 versionadas; snapshot 10 reimportado segundo o usuário; ainda não há link público nem todas as telas finais |
| Análises e achados finais | Parcial | Tasks 16 e 18 têm análises e limites documentados; faltam conclusões e recomendações finais |
| Vídeo pitch | Pendente | Não há roteiro, arquivo ou link |
| Certificados e elegibilidade da equipe | Não comprovado | Evidência externa ao repositório |

## 3. Requisitos eliminatórios

Todos os itens desta seção precisam estar concluídos. O atendimento parcial não habilita o trabalho para avaliação.

- [ ] **Pendente — Link público e funcional do aplicativo Qlik Sense.** Não há URL pública registrada.
- [x] **Visualização geográfica por município.** A Task 14 implementa mapa de pontos por valor líquido e mapa de áreas por valor por pessoa.
- [x] **Análise temporal dos repasses ou pagamentos.** A Task 15 apresenta créditos, ajustes e saldo líquido por mês.
- [x] **Pelo menos um KPI quantitativo.** Seis medidas mestras foram implementadas e validadas na pasta `Validação — Task 12` do aplicativo.
- [ ] **Pendente — Vídeo pitch público com até 5 minutos.** Não há vídeo nem link.
- [ ] **Parcial — Documento descritivo completo.** A contextualização, as bases e a metodologia planejada estão em [`edital-hackathon-qlik-2026.md`](./edital-hackathon-qlik-2026.md); faltam análises executadas, achados, conclusões e recomendações finais.
- [ ] **Não comprovado — Certificados das trilhas obrigatórias de todos os integrantes.** Não há comprovação no repositório.

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

- [ ] **Pendente — Calcular participação dos top 5, 10 e 20 municípios.**
- [ ] **Pendente — Comparar média, mediana, percentis e distribuição per capita.**
- [ ] **Parcial — Comparar municípios afetados com registros FUNDEC.** A Task 16 cruza os 478 nomes do extrato da Defesa Civil de 11/06/2024 com a base detalhada até 26/09/2024 e identifica 144 listados sem movimentação nessa base. A Tela 3 foi conferida no Qlik, exportada nos snapshots 09 e 10 e reimportada no snapshot 10 segundo o usuário. Falta corroboração externa dos casos antes de recomendações. Ausência de registro não demonstra ausência de atendimento.
- [ ] **Pendente — Definir critério reproduzível de subatendimento.**
- [ ] **Parcial — Analisar relação com IDH-M, PIB per capita, população e densidade.** A Task 18 concluiu a comparação descritiva entre IDH-M 2010 e valor líquido por habitante, com teste de sensibilidade por porte populacional. PIB per capita e densidade ainda não foram examinados nessa análise.
- [ ] **Pendente — Explicar limites e evitar interpretar correlação como causalidade.**

## 9. Dashboard e experiência no Qlik Sense

- [x] **Concluído — Criar página de visão geral com KPIs e narrativa.** (Task 13)
- [x] **Concluído — Criar página geográfica.** (Task 14)
- [x] **Concluído — Criar página temporal.** (Task 15)
- [x] **Concluído — Criar página de vulnerabilidade e repasses.** A Tela 5 da Task 18 mostra IDH-M 2010 × valor líquido por habitante, tabela municipal e nota metodológica; o usuário confirmou a reimportação do snapshot 10.
- [ ] **Pendente — Criar página de método, limitações e recomendações.**
- [x] **Concluído — Adicionar filtros úteis e consistentes entre páginas.** (Task 13)
- [ ] **Pendente — Implementar navegação e títulos dinâmicos.**
- [ ] **Parcial — Testar legibilidade, contraste, unidades, escalas e tooltips.** Tasks 14 e 15 possuem evidências visuais; falta auditoria final entre dispositivos.
- [ ] **Pendente — Exibir fonte, período e data de atualização.**
- [ ] **Pendente — Testar acesso público sem credenciais da equipe.**

## 10. Documento descritivo final

- [x] Contextualização do problema documentada.
- [x] Inventário das bases disponíveis documentado.
- [x] Metodologia planejada documentada.
- [ ] **Pendente — Atualizar a metodologia com o que foi realmente executado.**
- [ ] **Pendente — Inserir principais análises e achados com evidências.**
- [ ] **Pendente — Inserir conclusões que respondam às perguntas do edital.**
- [ ] **Pendente — Inserir recomendações diretamente ligadas aos achados.**
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
- [ ] **Não comprovado — Trilhas obrigatórias concluídas por todos até 10/09/2026.**
- [ ] **Não comprovado — Certificados reunidos e legíveis.**
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

1. Confirmar equipe, trilhas, certificados e responsável pela submissão.
2. Corrigir e validar o ETL.
3. Criar mapa, timeline e KPI no Qlik Sense.
4. Publicar e testar o link do aplicativo.
5. Finalizar documento descritivo e vídeo de até 5 minutos.

### Prioridade 1 — Garantir consistência analítica

1. Conciliar os totais das bases.
2. Tratar corretamente valores negativos.
3. Normalizar municípios com código IBGE.
4. Documentar métricas, períodos e limitações.
5. Revisar conclusões contra os dados de origem.

### Prioridade 2 — Buscar pontuação bônus

1. Incorporar indicador de impacto e marco temporal confiáveis.
2. Calcular métricas per capita e comparações normalizadas.
3. Cruzar repasses com vulnerabilidade socioeconômica.
4. Identificar desigualdades e lacunas por critério reproduzível.
5. Destacar insights originais e aplicáveis à tomada de decisão.

## 16. Critério para marcar este checklist como concluído

Um item só deve receber `[x]` quando houver evidência revisável: arquivo funcional, cálculo reproduzível, captura ou link testado, certificado ou registro de validação. Alegações sem evidência devem permanecer como pendentes ou não comprovadas.
