# Requisitos e status do projeto

## 1. Como ler este checklist

Este documento registra o estado do repositório em **8 de setembro de 2026**.

- `[x]` significa que há evidência verificável no repositório.
- `[ ] Parcial` significa que existe um artefato inicial, mas ele ainda não atende ao requisito completo.
- `[ ] Pendente` significa que o requisito ainda precisa ser implementado.
- `[ ] Não comprovado` significa que depende de informação, conta, certificado ou ação externa que não está versionada no repositório.

Um arquivo existente não é considerado concluído se estiver vazio, inconsistente com a estrutura atual ou sem evidência de funcionamento.

## 2. Resumo do estado atual

| Área | Estado | Evidência principal |
|---|---|---|
| Dados brutos do FUNDEC | Concluído | 658 movimentações e ranking de 334 municípios em `data/raw/csv/` |
| Dados de população e indicadores socioeconômicos | Concluído | SIDRA 2024 e base municipal com código IBGE, PIB e IDH-M |
| Documentação do problema e dos requisitos | Concluído | Documentos desta pasta |
| Pipeline de tratamento reproduzível | Parcial | Existe `etl/analis_de_dados.py`, mas caminhos, separadores e tipos não correspondem aos arquivos atuais |
| Banco analítico validado | Pendente | Nenhum banco versionado; arquivos `*.db` são ignorados pelo Git |
| Aplicativo e dashboard Qlik Sense | Pendente | Não há exportação, script final de carga nem link público no repositório |
| Análises e achados finais | Pendente | Não há resultados validados, conclusões ou recomendações finais |
| Vídeo pitch | Pendente | Não há roteiro, arquivo ou link |
| Certificados e elegibilidade da equipe | Não comprovado | Evidência externa ao repositório |

## 3. Requisitos eliminatórios

Todos os itens desta seção precisam estar concluídos. O atendimento parcial não habilita o trabalho para avaliação.

- [ ] **Pendente — Link público e funcional do aplicativo Qlik Sense.** Não há URL pública registrada.
- [ ] **Pendente — Visualização geográfica por município.** Os dados municipais existem, mas o mapa ainda não foi implementado.
- [ ] **Pendente — Análise temporal dos repasses ou pagamentos.** A base possui datas, mas não há timeline no Qlik Sense.
- [ ] **Pendente — Pelo menos um KPI quantitativo.** As métricas estão propostas, mas não implementadas no aplicativo.
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
- [ ] **Pendente — Criar instruções de execução que correspondam ao pipeline final.** O `README.md` atual descreve caminhos e um banco que não correspondem integralmente ao estado observado.
- [ ] **Pendente — Adicionar testes automatizados ou verificações reproduzíveis de qualidade dos dados.**
- [ ] **Pendente — Definir política para artefatos do Qlik e arquivos gerados.** Registrar o que será versionado e o que será publicado externamente.

## 5. Aquisição e cobertura dos dados

- [x] Base detalhada de repasses do FUNDEC disponível: `repasses_fundec_2024.csv`.
- [x] Ranking oficial por município disponível: `ranking_oficial_fundec_2024.csv`.
- [x] População estimada dos 497 municípios do RS disponível: `populacao_rs_2024.csv`.
- [x] Base municipal complementar com código IBGE, PIB, área, densidade e IDH-M disponível: `municipios-brasil.csv`.
- [x] Documentos legais e de referência disponíveis em `data/raw/pdf/`.
- [x] Bases auxiliares de recursos recebidos e convênios disponíveis.
- [ ] **Pendente — Registrar data de extração, URL exata, filtros e versão junto a cada arquivo.** O catálogo contém fontes, mas não toda a linhagem necessária para reprodução.
- [ ] **Pendente — Obter indicador de impacto por município.** Selecionar uma medida comparável, como pessoas afetadas, danos estimados, população desalojada ou reconhecimento de calamidade.
- [ ] **Pendente — Obter marco temporal por município.** Necessário para calcular dias entre evento crítico e primeiro repasse.

## 6. ETL e qualidade dos dados

- [x] Existe um script inicial de ETL: [`etl/analis_de_dados.py`](../etl/analis_de_dados.py).
- [ ] **Parcial — Leitura dos CSVs.** O script procura os arquivos em `data/raw/`, mas eles estão em `data/raw/csv/`; também usa separador `;` nas duas bases principais, que usam vírgula.
- [ ] **Pendente — Corrigir tipos de dados.** O script converte datas, valor e identificadores para `Int64`/texto em um mesmo laço. Data deve permanecer data, valor deve ser decimal com sinal e identificadores devem ser texto.
- [ ] **Pendente — Preservar estornos e ajustes.** Foram observadas 18 movimentações negativas; elas precisam ser interpretadas e mantidas no cálculo líquido.
- [ ] **Pendente — Conciliar bases principal e ranking.** A soma líquida observada na base detalhada é R$ 288.699.999,97, enquanto o ranking soma R$ 289.176.004,25. A diferença precisa ser explicada antes da publicação.
- [ ] **Pendente — Tratar o arquivo do SIDRA.** Remover metadados, cabeçalhos extras e notas de rodapé, preservando os 497 registros municipais.
- [ ] **Pendente — Criar chave municipal confiável.** Priorizar código IBGE e validar nomes sem acento ou com grafia divergente.
- [ ] **Pendente — Definir e tratar duplicidades.** Documentar a chave natural de uma movimentação e distinguir repetição legítima de duplicação.
- [ ] **Pendente — Criar relatório de qualidade.** Incluir contagens, nulos, intervalo de datas, valores negativos, duplicidades, municípios não associados e conciliação de totais.
- [ ] **Pendente — Gerar banco ou arquivos tratados de forma reproduzível.** O caminho documentado `database/banco_hackathon.db` não existe no repositório e `*.db` está no `.gitignore`.
- [ ] **Pendente — Validar o pipeline em ambiente limpo.** Instalar dependências, executar do zero e registrar a saída esperada.

## 7. Modelo de dados e carga no Qlik Sense

- [ ] **Pendente — Implementar `fato_repasses` com valor numérico assinado.**
- [ ] **Pendente — Implementar `dim_municipio` com código IBGE e atributos geográficos.**
- [ ] **Pendente — Implementar dimensão socioeconômica com ano de referência explícito.**
- [ ] **Pendente — Implementar calendário principal.**
- [ ] **Pendente — Incorporar dimensão ou indicador de impacto, caso a fonte seja obtida.**
- [ ] **Pendente — Criar script de carga do Qlik compatível com os artefatos gerados.**
- [ ] **Pendente — Evitar chaves sintéticas e associações circulares.** Validar o modelo no visualizador do Qlik.
- [ ] **Pendente — Registrar fórmulas e regras das medidas mestres.**
- [ ] **Pendente — Testar recarga completa e incremental, se aplicável.**

## 8. Análises exigidas e recomendadas

### 8.1 Distribuição geográfica

- [ ] **Pendente — Construir mapa municipal.**
- [ ] **Pendente — Exibir valor total e valor per capita.**
- [ ] **Pendente — Identificar maiores e menores recebedores com contexto.**
- [ ] **Pendente — Comparar repasse com indicador de impacto.** Depende da fonte ainda não incorporada.

### 8.2 Tempo de repasse

- [ ] **Pendente — Construir timeline de créditos e estornos.**
- [ ] **Pendente — Calcular a data do primeiro repasse por município.**
- [ ] **Pendente — Calcular dias desde o evento ou marco oficial.** Depende da fonte temporal municipal.
- [ ] **Pendente — Identificar municípios atendidos sistematicamente mais tarde.**

### 8.3 Concentração, lacunas e equidade

- [ ] **Pendente — Calcular participação dos top 5, 10 e 20 municípios.**
- [ ] **Pendente — Comparar média, mediana, percentis e distribuição per capita.**
- [ ] **Pendente — Identificar municípios atingidos sem repasse.** Depende da definição do universo de atingidos.
- [ ] **Pendente — Definir critério reproduzível de subatendimento.**
- [ ] **Pendente — Analisar relação com IDH-M, PIB per capita, população e densidade.**
- [ ] **Pendente — Explicar limites e evitar interpretar correlação como causalidade.**

## 9. Dashboard e experiência no Qlik Sense

- [ ] **Pendente — Criar página de visão geral com KPIs e narrativa.**
- [ ] **Pendente — Criar página geográfica.**
- [ ] **Pendente — Criar página temporal.**
- [ ] **Pendente — Criar página de equidade e vulnerabilidade.**
- [ ] **Pendente — Criar página de método, limitações e recomendações.**
- [ ] **Pendente — Adicionar filtros úteis e consistentes entre páginas.**
- [ ] **Pendente — Implementar navegação e títulos dinâmicos.**
- [ ] **Pendente — Testar legibilidade, contraste, unidades, escalas e tooltips.**
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
- [ ] **Não comprovado — Trilhas obrigatórias concluídas por todos.**
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
- [ ] **Pendente — Fazer uma única submissão pelo representante até 15/09/2026.**

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
