# Task 18 — Tela 5: vulnerabilidade e repasses (H3)

## Pergunta e universo

Entre os municípios com movimentações detalhadas do FUNDEC/RS, existe uma
associação descritiva entre o **IDH-M 2010** e o **valor líquido por habitante**
calculado com a população estimada de **2024**? A comparação usa o código IBGE
de sete dígitos (`chave_municipal`/`codigo_ibge`) para identificar municípios.

Os repasses abrangem **17/05/2024 a 26/09/2024**. A tabela
[`dim_municipio.csv`](../data/processed/dim_municipio.csv) contém os **334
municípios com movimentação** na base, dos quais **333 têm IDH-M 2010**.
**Pinto Bandeira (`4314548`)** não tem esse indicador na fonte compilada e
fica fora da comparação estatística; não foi atribuído valor estimado. Os 334
têm população 2024 positiva. O [catálogo de dados](../data/README.md)
identifica as fontes do IDH-M (Atlas Brasil, compilado pelo Atlas Cidade), da
população (IBGE/SIDRA) e das movimentações (FUNDEC/RS).

O universo contém apenas municípios com repasse registrado. Os 144 municípios
listados pela Defesa Civil sem movimentação **nesta base** aparecem na
[Task 16](./task-16-cobertura-lacunas.md), mas não possuem uma linha na
`dim_municipio.csv` atual. Por isso, esta análise não compara municípios
atendidos e não atendidos nem mede prioridade administrativa.

## Indicador e validação

Para cada município:

```text
reais_por_pessoa = soma dos valores assinados da tabela fato / população IBGE 2024
```

O numerador é o saldo líquido dos créditos e ajustes, inclusive os lançamentos
negativos. O denominador é a população municipal total, **não** o número de
pessoas atingidas. A soma municipal concilia com a tabela fato em
**R$ 288.699.999,97**. O cálculo reproduz os valores já presentes em
`valor_por_pessoa_2024`.

Execute na raiz do repositório:

```powershell
.\.venv\Scripts\python.exe etl/analise_idhm_repasses.py
```

O script verifica códigos únicos, população positiva, conciliação monetária e
o indicador por pessoa. Ele imprime os anos, cobertura, nulos, correlações e
faixas do IDH-M. As correlações abaixo são **descritivas**, calculadas sobre os
333 municípios com ambas as medidas e sem filtros no Qlik.

| Verificação | Resultado |
|---|---:|
| Correlação de Pearson, IDH-M × R$/pessoa | 0,0114 |
| Correlação de Spearman, IDH-M × R$/pessoa | −0,0776 |
| Municípios com população abaixo de 5.000 | 150 de 333 |
| Pearson com população ≥ 5.000 (183 municípios) | −0,1044 |
| Spearman com população ≥ 5.000 (183 municípios) | −0,1227 |

As faixas usam os quartis observados do IDH-M: **0,683**, **0,718** e
**0,746**. Valores iguais ao limite entram na faixa inferior.

| Faixa de IDH-M | Municípios | Mediana de R$/pessoa | Média de R$/pessoa |
|---|---:|---:|---:|
| Q1: 0,587–0,683 | 87 | R$ 69,95 | R$ 98,50 |
| Q2: 0,685–0,718 | 82 | R$ 56,53 | R$ 109,54 |
| Q3: 0,719–0,746 | 83 | R$ 77,67 | R$ 144,24 |
| Q4: 0,747–0,805 | 81 | R$ 57,96 | R$ 91,78 |

Não surge uma relação monotônica clara entre IDH-M histórico e valor líquido
por habitante neste recorte. Municípios pequenos podem ter valores altos por
pessoa mesmo com repasses absolutos moderados, razão para mostrar população e
revisar pontos extremos. A comparação de sensibilidade acima também não indica
uma associação forte. IDH-M 2010 não mede diretamente a pobreza em 2024, e
correlação não demonstra causalidade, necessidade ou efeito dos repasses.

## Montagem da Tela 5 no Qlik Cloud

Os campos necessários já estão no aplicativo; **não é preciso importar outro
CSV** para a primeira versão da tela. Após qualquer recarga, confira que
`dim_municipio` mantém `codigo_ibge`, `idhm_2010` e `populacao_2024`, associada
à `fato_repasses` somente por `chave_municipal`.

1. Crie a pasta **Tela 5 — Vulnerabilidade e repasses (H3)**.
2. Adicione um gráfico de dispersão. Use `municipio_ibge_2024` como dimensão,
   `Only(idhm_2010)` no eixo X, com três casas decimais, e
   `Sum(valor) / Only(populacao_2024)` no eixo Y, em R$/pessoa. Confira que
   Pinto Bandeira não aparece como ponto com IDH-M inventado.
3. Adicione uma tabela simples para auditoria, com nome, `codigo_ibge`,
   `idhm_2010`, `populacao_2024`, `Sum(valor)` e
   `Sum(valor) / Only(populacao_2024)`. Dê títulos legíveis às medidas.
4. Inclua uma nota visível: **IDH-M 2010; repasses FUNDEC de 17/05 a
   26/09/2024; população IBGE 2024; 333 municípios comparáveis sem filtros**.
   Explique que R$/pessoa usa a população total e que a associação não permite
   inferir causalidade ou prioridade administrativa. Se houver filtros, os
   números da análise acima representam somente o estado **sem filtros**.
5. Valide o total líquido, a exclusão de Pinto Bandeira, pontos extremos e
   alguns municípios contra `dim_municipio.csv` e `fato_repasses.csv`.

O [manual do Qlik para gráfico de dispersão](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/Visualizations/ScatterPlot/create-scatter-plots.htm)
confirma a configuração de uma dimensão e duas medidas. A
[tabela simples](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/Visualizations/StraightTable/create-sn-straight-tables.htm)
permite mostrar os campos de auditoria lado a lado.

## Ajustes herdados da Task 16 e evidência final

Antes de exportar o próximo snapshot, melhore a legibilidade da Tela 3:
substitua ou complemente a tabela dinâmica por uma tabela simples que exiba
diretamente município, código IBGE, situação na lista, situação na base,
quantidade de movimentações e saldo líquido. Registre uma captura sem filtros
e outra com `afetado_sem_registro` selecionado. Preserve a nota de que
**ausência de registro FUNDEC não equivale a ausência de atendimento**.

Depois de validar as duas telas, exporte o aplicativo **com dados** no
snapshot sequencial **10**, registre tamanho e SHA-256 e reimporte o QVF para
conferir modelo, medidas e visualizações restaurados. A reimportação do
[snapshot 09](../qlik/versoes-do-app/09-task-16/README.md) ainda não foi
confirmada; o teste do snapshot 10 deve cobrir também as funcionalidades da
Tela 3. Registre as capturas, resultados de conferência e limitações antes de
marcar esta task como concluída.
