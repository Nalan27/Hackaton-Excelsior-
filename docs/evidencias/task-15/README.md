# Evidências da Task 15 — Tela 2 (Linha do Tempo)

**Estado:** capturas do Qlik Cloud pendentes no PR #40. Este arquivo é um roteiro de conferência; ele não substitui os prints reais do aplicativo.

## Capturas a incluir

| Arquivo | O que deve aparecer |
|---|---|
| `01-tela2-evolucao-mensal.png` | Tela 2 em modo de visualização, sem filtros; título, eixo de 202405 a 202409 em ordem cronológica, legenda e séries de créditos, ajustes negativos e saldo líquido. |
| `02-tela2-filtro.png` | A mesma tela após selecionar um mês ou município, com seleção e valores resultantes visíveis. Registrar abaixo qual seleção foi usada. |

**Seleção usada no segundo print:** preencher após a captura.

## Valores de referência

Calculados a partir de `data/processed/fato_repasses.csv`, agrupando as movimentações por mês da coluna `data`. Créditos são valores positivos; ajustes são valores negativos; saldo líquido é a soma dos dois.

| Mês | Créditos | Ajustes negativos | Saldo líquido |
|---|---:|---:|---:|
| 2024-05 | R$ 47.000.000,00 | −R$ 4.800.000,00 | R$ 42.200.000,00 |
| 2024-06 | R$ 166.625.581,37 | −R$ 1.869.767,44 | R$ 164.755.813,93 |
| 2024-07 | R$ 80.289.534,88 | −R$ 11.565.116,28 | R$ 68.724.418,60 |
| 2024-08 | R$ 6.617.441,86 | −R$ 400.000,00 | R$ 6.217.441,86 |
| 2024-09 | R$ 6.802.325,58 | R$ 0,00 | R$ 6.802.325,58 |
| **Total** | **R$ 307.334.883,69** | **−R$ 18.634.883,72** | **R$ 288.699.999,97** |

O print do Qlik precisa permitir conferir o resultado exibido com esta tabela, considerando a escala e o arredondamento do gráfico. Se o app apresentar valores diferentes, registrar a seleção ativa ou investigar a divergência antes de concluir a task.

## Conferência após incluir as imagens

- [ ] Os dois arquivos PNG foram adicionados a esta pasta e abrem normalmente.
- [ ] A ordem do eixo e as três medidas são legíveis no primeiro print.
- [ ] A seleção e o efeito sobre os valores são legíveis no segundo print.
- [ ] Os totais exibidos no app foram confrontados com os valores de referência.
- [ ] O README do snapshot 06 foi atualizado com o resultado da conferência.
