# Task 12 — cálculos reutilizáveis

## Objetivo

Padronizar no Qlik Sense as medidas usadas em todo o aplicativo, garantir que
elas respondam corretamente aos filtros e registrar evidências de que o modelo
não possui tabelas isoladas, chaves sintéticas ou associações circulares.

O catálogo normativo das expressões está em
[`qlik/medidas-mestras.md`](../qlik/medidas-mestras.md).

## Medidas definidas

| Medida | Regra resumida | Resultado sem filtros |
|---|---|---:|
| Valor líquido recebido | Créditos e ajustes com sinal | R$ 288.699.999,97 |
| Créditos recebidos | Somente `valor > 0` | R$ 307.334.883,69 |
| Ajustes negativos | Somente `valor < 0`, preservando o sinal | R$ -18.634.883,72 |
| Municípios atendidos | Chaves municipais distintas | 334 |
| Valor líquido por pessoa | Total líquido / população única dos municípios | R$ 32,89 |
| Tempo médio até o primeiro repasse | Média dos intervalos municipais válidos | 40,13 dias |

Os cálculos de valor partem de `fato_repasses.valor`, evitando o uso de totais
pré-calculados que não responderiam adequadamente aos filtros de data ou
recurso. O denominador per capita agrega uma população por município antes da
divisão e não soma razões municipais.

## Conciliação

A base detalhada totaliza R$ 288.699.999,97 e o ranking oficial totaliza
R$ 289.176.004,25. A diferença de R$ -476.004,28 está registrada em
`data/processed/conciliacao.csv` e concentrada em três municípios:

| Município | Diferença entre fato e ranking |
|---|---:|
| São Sebastião do Caí | R$ -200.000,00 |
| Canoas | R$ -176.004,28 |
| Harmonia | R$ -100.000,00 |

A base detalhada é a fonte operacional das medidas porque contém as 658
movimentações individualizadas, incluindo 18 ajustes negativos. O ranking é
mantido como referência de conciliação. A diferença é explicitada, não
compensada ou ocultada.

## Validações automatizadas

`tests/test_etl_outputs.py` confere:

- créditos, ajustes negativos e valor líquido globais;
- identidade entre créditos, ajustes e total líquido;
- quantidade de municípios atendidos;
- população agregada e valor líquido por pessoa;
- tempo médio municipal;
- seleção conjunta de Porto Alegre e Canoas, comprovando a divisão dos totais
  agregados;
- preservação dos 18 valores negativos;
- três divergências da conciliação;
- integridade das associações previstas no modelo.

Execução:

```powershell
.\.venv\Scripts\python.exe etl\analis_de_dados.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Validação necessária no Qlik Cloud

A parte abaixo exige acesso ao aplicativo e deve ser executada antes de
encerrar a issue.

1. Criar como itens mestres as seis medidas do catálogo.
2. Criar uma pasta `Validação — Task 12` com seis KPIs, filtros de município,
   data e recurso, e uma tabela de conferência.
3. Conferir os valores sem filtros contra a tabela deste documento.
4. Filtrar Porto Alegre e confirmar: créditos R$ 16.247.674,42, ajustes
   R$ -10.465.116,28, líquido R$ 5.782.558,14, R$ 4,16 por pessoa e 84 dias.
5. Filtrar Canoas e confirmar: líquido R$ 5.782.558,14, R$ 16,08 por pessoa e
   57 dias.
6. Selecionar Porto Alegre e Canoas juntos e confirmar R$ 11.565.116,28 de
   valor líquido, população de 1.748.876 e R$ 6,61 por pessoa.
7. Aplicar filtros de data e recurso e verificar que as medidas monetárias e
   per capita respondem às seleções.
8. Abrir o visualizador do modelo e confirmar quatro tabelas associadas,
   nenhuma tabela isolada, nenhuma chave sintética e nenhum ciclo.

O modelo esperado é:

```text
dim_municipio (chave_municipal)
├── fato_repasses (chave_municipal) ── data ── dim_calendario
└── intervalo_primeiro_repasse (chave_municipal)
```

Somente `dim_municipio.csv`, `fato_repasses.csv`, `dim_calendario.csv` e
`intervalo_primeiro_repasse.csv` devem formar o modelo analítico. Arquivos de
validação, conciliação ou documentação não devem ser carregados como tabelas.

## Evidências para conclusão

As capturas devem ser adicionadas em `docs/evidencias/task-12/`:

1. `01-medidas-mestras.png` — lista das seis medidas mestras;
2. `02-validacao-sem-filtros.png` — KPIs globais;
3. `03-validacao-porto-alegre.png` — conferência do caso com estornos;
4. `04-validacao-selecao-multipla.png` — Porto Alegre e Canoas;
5. `05-modelo-sem-tabelas-soltas.png` — quatro tabelas associadas.

Depois da validação, exportar o aplicativo **com dados** para
`qlik/versoes-do-app/04-task-12/app.qvf`, registrar tamanho e SHA-256 no README
da versão e confirmar o rastreamento pelo Git LFS.

## Estado

A definição das medidas, a conciliação e as verificações automatizadas estão
versionadas. Em 15/09/2026, o ETL foi executado com todas as validações
críticas aprovadas e os 20 testes automatizados passaram. A conclusão depende
da criação dos itens mestres, das conferências visuais no Qlik Cloud e da
exportação do snapshot com dados.
