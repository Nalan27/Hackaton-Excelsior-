# Edital explicado e especificação do projeto

## 1. Sobre este documento

Este documento transforma o conteúdo legível do **Edital do 2º Hackathon Unicesumar em parceria com a Qlik** em uma especificação de trabalho para a equipe.

Ele não substitui o edital original. A [atualização de submissão comunicada em 18/09/2026](./atualizacao-submissao-2026-09-18.md) prevalece sobre as instruções anteriores de entrega quando houver conflito. Em caso de dúvida, deve prevalecer a orientação da Comissão Organizadora.

Alguns elementos gráficos do PDF fornecido, principalmente parte da coluna de pesos da rubrica e os links embutidos nos módulos de aprendizagem, não estavam legíveis. Esses pontos estão identificados para conferência no arquivo original, sem preenchimento por suposição.

## 2. Resumo executivo

O desafio é construir, no **Qlik Sense**, uma análise visual, interativa e narrativa sobre a distribuição de recursos públicos para a reconstrução do Rio Grande do Sul após as enchentes de 2024.

A base principal deve ser composta pelos pagamentos e repasses do **Fundo Estadual de Defesa Civil do Rio Grande do Sul (FUNDEC/RS)**. Bases públicas complementares podem e devem ser incorporadas quando ajudarem a explicar impacto, vulnerabilidade, população, capacidade econômica ou desigualdade entre os municípios.

O produto final precisa transformar dados públicos em evidências úteis para a tomada de decisão. Não basta mostrar valores: a equipe deve explicar padrões, lacunas, concentrações, atrasos e possíveis desigualdades, apresentando conclusões e recomendações sustentadas pelos dados.

## 3. Tema e problema central

**Tema:** Transparência e equidade na reconstrução do Rio Grande do Sul.

As enchentes de 2024 formaram uma das maiores crises climáticas da história do Brasil. A resposta exigiu a mobilização de recursos públicos para socorro, recuperação e reconstrução dos municípios atingidos.

O problema proposto pelo edital pode ser resumido em quatro perguntas:

1. Como os recursos foram distribuídos entre os municípios afetados?
2. A distribuição refletiu as necessidades sociais, econômicas e estruturais das populações atingidas?
3. Existem padrões de concentração, desigualdades, lacunas ou anomalias relevantes?
4. Os municípios mais vulneráveis foram atendidos proporcionalmente no processo de reconstrução?

## 4. Objetivo do projeto

Criar uma aplicação no Qlik Sense que combine análise visual e narrativa para:

- tornar os repasses do FUNDEC/RS compreensíveis e rastreáveis;
- comparar municípios por valor recebido, população, vulnerabilidade e outros indicadores relevantes;
- identificar padrões geográficos e temporais;
- apontar municípios possivelmente subatendidos ou com recebimento muito abaixo do padrão comparável;
- avaliar a concentração dos recursos;
- produzir recomendações aplicáveis à gestão pública e à alocação futura de recursos.

## 5. Perguntas analíticas prioritárias

### 5.1 Distribuição geográfica

- Quais municípios receberam os maiores e os menores valores?
- Quantos municípios receberam recursos?
- Os valores acompanham a dimensão do impacto sofrido?
- Existem regiões com baixa cobertura ou concentração atípica?

### 5.2 Velocidade dos repasses

- Em quais datas ocorreram os pagamentos?
- Quanto tempo transcorreu entre o evento crítico e o primeiro repasse a cada município?
- Existem municípios sistematicamente atendidos mais tarde?
- O ritmo dos repasses mudou ao longo do período analisado?

> Para medir o tempo entre impacto e pagamento de forma válida, ainda é necessária uma fonte que registre a data do evento, do reconhecimento de emergência ou de outro marco comparável para cada município. A data do pagamento, isoladamente, não permite calcular esse atraso.

### 5.3 Lacunas e subatendimento

- Há municípios atingidos sem registro de repasse?
- Quais receberam valores muito abaixo de municípios com impacto ou perfil semelhante?
- Há inconsistências, estornos ou registros que precisam de tratamento antes da comparação?

### 5.4 Concentração dos recursos

- Qual é a participação dos 5, 10 e 20 municípios com maiores valores?
- A distribuição é equilibrada ou concentrada em municípios de maior porte?
- A concentração muda quando o valor é analisado por habitante?

### 5.5 Vulnerabilidade socioeconômica — análise avançada

- Municípios com menor IDH-M foram priorizados?
- Existe relação entre repasse per capita, população, PIB per capita, densidade e IDH-M?
- Quais municípios combinam alta vulnerabilidade com baixo repasse relativo?

## 6. Público-alvo da solução

A aplicação deve ser compreensível para diferentes públicos:

- gestores públicos e equipes de Defesa Civil;
- órgãos de controle e transparência;
- pesquisadores e analistas de políticas públicas;
- cidadãos e organizações da sociedade civil;
- avaliadores do Hackathon.

A narrativa deve permitir que uma pessoa não técnica entenda o problema, explore os dados e chegue às principais conclusões sem depender de explicação externa.

## 7. Dados disponíveis no repositório

O inventário abaixo descreve o estado atual, não uma garantia de que todos os arquivos já estejam limpos e prontos para uso.

| Artefato | Conteúdo | Situação observada |
|---|---|---|
| `data/raw/csv/repasses_fundec_2024.csv` | 658 movimentações, 334 municípios, datas entre 17/05/2024 e 26/09/2024, recursos do Tesouro e do Judiciário | Base principal disponível; contém 18 valores negativos que precisam ser tratados como possíveis estornos ou ajustes, e não descartados automaticamente |
| `data/raw/csv/ranking_oficial_fundec_2024.csv` | Ranking de 334 municípios por valor pago | Disponível; o total não coincide exatamente com a soma líquida calculada a partir da base detalhada e exige conciliação |
| `data/raw/csv/populacao_rs_2024.csv` | População estimada dos 497 municípios do RS em 2024 | Disponível em formato de exportação do SIDRA, com cabeçalhos e notas extras que precisam ser removidos no ETL |
| `data/raw/csv/municipios-brasil.csv` | 5.571 municípios brasileiros, incluindo os 497 do RS; código IBGE, população, PIB, área, densidade e IDH-M | Disponível; permite o cruzamento socioeconômico, respeitando o ano de referência de cada indicador |
| `data/raw/csv/Recursos Recebidos.csv` | Registros auxiliares de recursos recebidos | Disponível; deve ter sua relevância e granularidade validadas antes de entrar no modelo |
| `data/raw/csv/Convênios e outros acordos firmados.csv` | Registros auxiliares de convênios | Disponível; deve ter sua relação com o escopo FUNDEC/RS validada |
| `data/raw/pdf/` | Legislação e documentos de referência | Disponíveis para contextualização e validação jurídica; não são fatos transacionais do modelo analítico |
| `fundec_querydata_capture.json` | Captura adicional relacionada à consulta de dados do FUNDEC | Disponível; estrutura e procedência ainda precisam ser documentadas antes do uso |

As fontes e os respectivos endereços públicos estão catalogados em [`data/README.md`](../data/README.md).

### 7.1 Alertas de qualidade já identificados

- O arquivo detalhado possui valores positivos e negativos. O campo deve ser convertido para número decimal com sinal preservado.
- CNPJ, processo e empenho são identificadores e devem ser tratados como texto, evitando perda de zeros e operações aritméticas indevidas.
- Os nomes dos municípios aparecem sem acentos em parte das fontes. A junção deve usar código IBGE sempre que possível; quando não houver código, deve usar uma chave normalizada e uma tabela de correspondência validada.
- A soma líquida observada nos 658 registros detalhados é diferente do total do ranking. Antes de publicar KPIs, a equipe deve investigar período de referência, filtros, estornos e versão das fontes.
- População, PIB e IDH-M têm anos de referência distintos. O dashboard deve exibir esses anos e evitar sugerir que todos os indicadores são contemporâneos.
- A base atual não contém, de forma explícita, a intensidade do impacto das enchentes por município nem o marco inicial necessário para calcular o tempo de resposta.

## 8. Modelo de dados recomendado

Uma estrutura em estrela facilita o uso no Qlik Sense:

| Tabela lógica | Finalidade | Campos principais |
|---|---|---|
| `fato_repasses` | Uma linha por movimentação financeira | data, processo, recurso, empenho, CNPJ, credor, município, código IBGE, valor com sinal |
| `dim_municipio` | Cadastro único dos municípios | código IBGE, nome oficial, região/intermediária, população, área e densidade |
| `dim_socioeconomica` | Indicadores e seus anos de referência | código IBGE, IDH-M 2010, PIB 2023, PIB per capita e populações disponíveis |
| `dim_calendario` | Análise temporal consistente | data, ano, trimestre, mês, semana e marcadores do evento |
| `dim_impacto` | Comparação entre necessidade e repasse | código IBGE, data do impacto, pessoas afetadas, danos ou outro indicador selecionado |

### 8.1 Regras mínimas de transformação

1. Preservar os arquivos brutos sem alteração.
2. Padronizar nomes de colunas e tipos em uma camada tratada.
3. Converter valores monetários brasileiros para decimal, mantendo os sinais negativos.
4. Validar datas inválidas, duplicidades e campos obrigatórios.
5. Criar uma chave municipal estável baseada no código IBGE.
6. Registrar a fonte e o ano de cada indicador.
7. Conciliar o total detalhado com o ranking oficial ou documentar claramente a diferença.
8. Produzir um relatório de qualidade antes da carga no Qlik Sense.

## 9. Indicadores recomendados

### 9.1 KPIs principais

- valor líquido pago;
- valor bruto de créditos;
- total de estornos ou ajustes negativos;
- número de movimentações;
- número de municípios atendidos;
- valor médio e mediano por município;
- valor pago por habitante;
- participação dos 10 maiores recebedores;
- dias até o primeiro repasse, quando a data de referência estiver disponível.

### 9.2 Indicadores comparativos

- participação do município no total de repasses;
- participação do município na população atingida;
- razão entre participação nos repasses e participação na necessidade estimada;
- percentil de repasse total e per capita;
- distância em relação à mediana de municípios comparáveis;
- correlação entre repasse per capita e IDH-M, PIB per capita, população ou indicador de impacto.

Nenhuma correlação deve ser apresentada como causalidade. Comparações precisam declarar filtros, universo, período e limitações.

## 10. Estrutura recomendada do aplicativo Qlik Sense

### Página 1 — Visão geral

- KPIs de valor, municípios, movimentações e período;
- texto curto explicando o problema;
- filtros globais por município, data, recurso e faixa de vulnerabilidade;
- destaques com os principais achados.

### Página 2 — Mapa da distribuição

- mapa por município;
- alternância entre valor total, valor per capita e outro indicador normalizado;
- ranking e participação no total;
- tooltip com contexto socioeconômico e fonte.

### Página 3 — Linha do tempo

- evolução diária, semanal ou mensal dos pagamentos;
- créditos e estornos diferenciados;
- primeiro pagamento por município;
- marcadores de eventos relevantes, quando a fonte temporal for incorporada.

### Página 4 — Equidade e vulnerabilidade

- dispersões entre repasse e indicadores socioeconômicos;
- comparação por quadrantes ou grupos equivalentes;
- municípios potencialmente subatendidos;
- explicação metodológica dos limites da comparação.

### Página 5 — Qualidade, método e recomendações

- bases utilizadas, períodos e data da atualização;
- regras de limpeza e conciliação;
- limitações conhecidas;
- conclusões e recomendações sustentadas pelas visualizações anteriores.

## 11. Metodologia de análise

1. **Aquisição:** registrar URL, órgão, data de acesso e versão de cada fonte.
2. **Perfilamento:** medir cobertura, nulos, duplicidades, formatos, intervalos e totais.
3. **Limpeza:** padronizar tipos, valores monetários, datas e chaves municipais.
4. **Conciliação:** comparar ranking e movimentações detalhadas, investigando diferenças.
5. **Enriquecimento:** associar código IBGE, população e indicadores socioeconômicos.
6. **Construção de métricas:** definir fórmulas, denominadores, filtros e anos de referência.
7. **Análise exploratória:** procurar padrões geográficos, temporais, concentração, lacunas e anomalias.
8. **Validação:** revisar amostras contra as fontes, testar totais e submeter achados à revisão da equipe.
9. **Storytelling:** ordenar as evidências do problema à recomendação, evitando gráficos sem interpretação.
10. **Entrega:** testar filtros, navegação e legibilidade no aplicativo; conferir o acesso público como leitor à pasta do Drive, ao documento e ao vídeo.

## 12. Entregáveis e forma de envio atualizados

Conforme a [orientação recebida em 18/09/2026](./atualizacao-submissao-2026-09-18.md), cada equipe cria uma pasta pública no Google Drive com o nome oficial da equipe, configurada como **Qualquer pessoa com o link — Leitor**. Todos os arquivos da entrega devem estar nela. Um único integrante envia o projeto pela [Central Hackathon](https://fabioacs.github.io/painel-hackathon); somente quem enviou pode atualizá-lo até o prazo final.

A pasta deve conter, no mínimo:

1. **Documento de texto** com contexto do problema, bases utilizadas, metodologia, principais achados, conclusões e recomendações fundamentadas. O documento deve trazer prints do dashboard com uma visualização geográfica por município, uma análise temporal dos repasses ou pagamentos e um KPI quantitativo, além da explicação de cada gráfico apresentado.
2. **Vídeo pitch** de até cinco minutos, com navegação pelo dashboard. Quem apresentar deve aparecer no vídeo; a apresentação não pode ter narração por IA. A equipe escolhe os apresentadores, sem obrigação de todos aparecerem.

O link público do Qlik Sense e os vídeos individuais dos integrantes para comprovar trilhas foram dispensados. O comunicado não afirma que os certificados das trilhas foram dispensados; a equipe deve preservá-los e confirmar se precisam acompanhar a entrega.

## 13. Checklist da entrega atualizada

Antes do envio, conferir:

1. pasta pública do Drive com nome da equipe e permissão de leitor para qualquer pessoa com o link;
2. documento de texto com todos os itens mínimos, prints visíveis e explicação de cada gráfico;
3. vídeo com até cinco minutos, navegação pelo dashboard, apresentador visível e sem narração por IA;
4. acesso ao documento e ao vídeo fora das contas da equipe;
5. um único representante responsável pelo envio e por eventuais atualizações;
6. submissão pela Central Hackathon até 23/09/2026 e comprovante guardado.

A exigência residual de certificados deve ser confirmada com a organização; a dispensa de vídeos individuais não equivale à dispensa das trilhas.

## 14. Critérios de avaliação

Os projetos habilitados recebem notas inteiras de 0 a 10 por critério, por múltiplos avaliadores independentes. A nota final considera a média das avaliações e os pesos da rubrica, acrescida de bônus quando aplicável.

Os critérios legíveis no edital são:

- clareza da narrativa analítica;
- qualidade das conclusões;
- qualidade do vídeo pitch;
- qualidade das visualizações;
- uso dos recursos do Qlik Sense, incluindo interatividade, filtros e navegação;
- profundidade analítica;
- consistência metodológica;
- relevância dos insights e recomendações.

> A coluna de pesos do PDF fornecido não ficou legível de forma confiável, com exceção de “Consistência metodológica — 10%”. Os demais pesos devem ser confirmados diretamente no edital original ou com a organização antes da priorização final.

### 14.1 Bônus de análise avançada

O edital prevê até **5 pontos adicionais** para aprofundamento analítico:

| Critério | Evidência esperada | Referência recuperada* |
|---|---|---:|
| Correlação com vulnerabilidade socioeconômica | Cruzamento com indicadores sociais, econômicos ou demográficos | +2 pontos |
| Sofisticação analítica | Comparações, indicadores per capita, normalizações, índices ou relações estatísticas | +1 ponto |
| Identificação de desigualdades e lacunas | Evidência de municípios subatendidos, inconsistências ou distorções | +1 ponto |
| Originalidade dos insights | Descobertas relevantes ou interpretações pouco óbvias | +1 ponto |

\* Os valores individuais foram recuperados de uma tabela parcialmente legível e totalizam o limite de 5 pontos informado no texto. Devem ser conferidos no edital original antes da entrega.

O módulo recomendado “Criando o Calendário Principal”, voltado à análise temporal, é opcional e tem duração indicada de 4h24.

### 14.2 Desempate

Em caso de empate, a ordem indicada é:

1. maior nota em profundidade analítica;
2. maior nota em relevância dos insights e recomendações;
3. maior nota em clareza da narrativa analítica.

### 14.3 O que evitar e o que valorizar

Não são diferenciais:

- excesso de gráficos sem interpretação;
- dashboards visualmente poluídos ou pouco legíveis;
- conclusões sem sustentação nos dados;
- conteúdo gerado por inteligência artificial sem validação e contextualização da equipe.

São especialmente valorizados:

- storytelling orientado por evidências;
- comunicação visual clara e objetiva;
- identificação de desigualdades e lacunas;
- comparações metodologicamente justificadas;
- insights aplicáveis a políticas públicas e tomada de decisão.

## 15. Cronograma do evento

Os períodos de workshops e cursos foram informados pela equipe. O prazo de entrega foi posteriormente prorrogado no comunicado da organização recebido em 18/09/2026.

| Etapa | Período |
|---|---|
| Inscrição das equipes | 29/06 a 27/07/2026 |
| Workshops | De 03/08 a 24/08/2026 |
| Cursos na Qlik | De 29/06 a 10/09/2026 |
| Submissão final do desafio | Até 23/09/2026; horário-limite não informado |
| Seleção interna dos 10 melhores trabalhos | A confirmar após a atualização do prazo de entrega |
| Apresentação e premiação | 07/10/2026, conforme o PDF; atualização não informada |

O prazo de conclusão dos cursos informado pela equipe é **10/09/2026**. O prazo final de submissão comunicado pela organização é **23/09/2026**, sem horário-limite especificado na mensagem recebida.

O PDF indicava seleção interna de 16/09 a 30/09/2026. Como esse período começa antes do prazo de entrega prorrogado, sua atualização ainda precisa ser confirmada. A inscrição e a apresentação/premiação permanecem registradas como referência do PDF.

## 16. Participação e formação da equipe

- evento realizado de forma on-line;
- equipes com no mínimo 3 e no máximo 5 integrantes;
- todos devem ser estudantes regularmente matriculados e ativos na modalidade EaD, em um dos cursos de TI listados no edital;
- apenas um integrante realiza a inscrição e a submissão em nome da equipe;
- limite indicado de 300 equipes, respeitada a ordem cronológica das inscrições validadas;
- colaboradores da Unicesumar não podem participar;
- todos os integrantes precisam concluir as trilhas obrigatórias e apresentar os certificados.

O edital lista cursos como Análise e Desenvolvimento de Sistemas, Banco de Dados, Segurança Cibernética/Cibersegurança, Ciência de Dados e Análise de Comportamento, Desenvolvimento de Aplicativos Móveis, Engenharia de Software, Gestão em Tecnologia da Informação, Inteligência Artificial e Machine Learning, Jogos Digitais, Redes de Computadores e Sistemas para Internet. A elegibilidade individual deve ser confirmada no original.

## 17. Premiação

- 1º lugar: R$ 7.000,00 por equipe;
- 2º lugar: R$ 5.000,00 por equipe;
- 3º lugar: R$ 3.000,00 por equipe.

O valor é dividido igualmente entre os integrantes, com pagamento individual por CPF, podendo ocorrer em até 90 dias após o encerramento oficial e a validação administrativa.

## 18. Originalidade, autoria e uso de inteligência artificial

O trabalho deve ser original e desenvolvido pelos participantes durante o período do Hackathon. O uso de inteligência artificial é permitido, mas deve ser declarado no documento descritivo, contendo:

- ferramenta utilizada;
- finalidade do uso;
- etapas em que a ferramenta participou;
- forma de validação humana.

A IA não substitui a responsabilidade analítica da equipe. Plágio, uso indevido de conteúdo protegido, submissão de projeto não original ou análise incompatível com o domínio demonstrado pela equipe podem causar desclassificação.

### Declaração preliminar para este repositório

O OpenAI Codex foi utilizado para auxiliar na extração do conteúdo legível do edital, na reorganização desta documentação e na auditoria dos artefatos existentes no repositório. A equipe ainda deve revisar o texto, confirmar os trechos sinalizados e validar humanamente toda análise, cálculo, conclusão e recomendação antes da submissão.

## 19. ODS relacionados

O edital relaciona o desafio aos seguintes Objetivos de Desenvolvimento Sustentável:

- ODS 4 — Educação de Qualidade;
- ODS 8 — Trabalho Decente e Crescimento Econômico;
- ODS 9 — Indústria, Inovação e Infraestrutura;
- ODS 11 — Cidades e Comunidades Sustentáveis;
- ODS 13 — Ação Contra a Mudança Global do Clima.

## 20. Definição de projeto concluído

O projeto só deve ser considerado finalizado quando:

- o pipeline de dados for reproduzível e documentado;
- os totais e divergências forem validados;
- as análises obrigatórias estiverem implementadas no Qlik Sense;
- o dashboard estiver claro e navegável para a gravação do pitch;
- os achados tiverem evidência rastreável e limitações explícitas;
- o documento no Drive contiver resultados, conclusões, recomendações, prints e explicações de cada gráfico;
- o vídeo no Drive tiver até cinco minutos, navegação pelo dashboard, apresentador visível e nenhuma narração por IA;
- os certificados tiverem sido reunidos enquanto sua exigência residual é confirmada;
- a declaração de uso de IA tiver sido revisada;
- uma segunda pessoa tiver executado o checklist e testado o acesso à pasta, ao documento e ao vídeo fora das contas da equipe.

O acompanhamento detalhado desses pontos está em [`requisitos-e-status.md`](./requisitos-e-status.md).
