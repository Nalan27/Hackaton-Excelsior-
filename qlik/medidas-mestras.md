# Medidas mestras do aplicativo Qlik

Este catálogo é a referência da Task 12 para os cálculos reutilizados no
aplicativo. As expressões devem ser criadas como **itens mestres** no Qlik
Sense. Gráficos e KPIs devem reutilizar esses itens, em vez de manter cópias
independentes das expressões.

## 1. Valor líquido recebido

- **Nome:** `Valor líquido recebido`
- **Expressão:**

  ```qlik
  Sum(valor)
  ```

- **Formato:** moeda brasileira, com duas casas decimais.
- **Regra:** soma todas as movimentações da seleção, preservando créditos
  positivos e ajustes negativos.
- **Valor sem filtros:** R$ 288.699.999,97.

Esta é a medida principal de valor do aplicativo. O campo `valor` da tabela
`fato_repasses` é usado para que filtros de data, município e recurso sejam
respeitados.

## 2. Créditos recebidos

- **Nome:** `Créditos recebidos`
- **Expressão:**

  ```qlik
  Sum({$<valor={">0"}>} valor)
  ```

- **Formato:** moeda brasileira, com duas casas decimais.
- **Regra:** soma somente movimentações positivas.
- **Valor sem filtros:** R$ 307.334.883,69.

## 3. Ajustes negativos

- **Nome:** `Ajustes negativos`
- **Expressão:**

  ```qlik
  Sum({$<valor={"<0"}>} valor)
  ```

- **Formato:** moeda brasileira, preservando o sinal negativo.
- **Regra:** soma os 18 estornos ou ajustes negativos. A medida principal não
  usa `Abs()`, para não ocultar a natureza do movimento.
- **Valor sem filtros:** R$ -18.634.883,72.

A seguinte identidade deve valer em qualquer seleção:

```text
Créditos recebidos + Ajustes negativos = Valor líquido recebido
```

## 4. Municípios atendidos

- **Nome:** `Municípios atendidos`
- **Expressão:**

  ```qlik
  Count(DISTINCT chave_municipal)
  ```

- **Formato:** inteiro.
- **Regra:** conta as chaves municipais distintas associadas à seleção.
- **Valor sem filtros:** 334.

## 5. Valor líquido por pessoa

- **Nome:** `Valor líquido por pessoa`
- **Expressão:**

  ```qlik
  If(
      Sum(Aggr(Only(populacao_2024), chave_municipal)) > 0,
      Sum(valor)
      /
      Sum(Aggr(Only(populacao_2024), chave_municipal))
  )
  ```

- **Formato:** moeda brasileira por pessoa, com duas casas decimais.
- **Numerador:** valor líquido da seleção.
- **Denominador:** soma de uma única população IBGE/SIDRA 2024 para cada
  município associado à seleção.
- **Valor sem filtros:** R$ 32,89 por pessoa.

A expressão agrega primeiro os totais e só depois efetua a divisão. Não usar
`Sum(valor_por_pessoa_2024)`, pois a soma de razões municipais não representa
o valor por pessoa do conjunto selecionado.

## 6. Tempo médio até o primeiro repasse

- **Nome:** `Tempo médio até o primeiro repasse`
- **Expressão:**

  ```qlik
  Avg(
      {$<status_intervalo={"ok"}>}
      intervalo_desde_marco_adotado_dias
  )
  ```

- **Formato:** número com duas casas decimais e sufixo `dias`.
- **Regra:** média simples dos intervalos municipais publicáveis; cada
  município possui uma observação em `intervalo_primeiro_repasse`.
- **Valor sem filtros:** 40,13 dias.

O intervalo parte do marco estadual comum de 24/04/2024 e termina no primeiro
crédito positivo. Ele não mede tempo desde o impacto local, solicitação,
habilitação ou ordem bancária.

## Conciliação das fontes

| Fonte | Total |
|---|---:|
| Movimentações detalhadas | R$ 288.699.999,97 |
| Ranking oficial | R$ 289.176.004,25 |
| Detalhada menos ranking | R$ -476.004,28 |

A divergência está concentrada em São Sebastião do Caí (R$ -200.000,00),
Canoas (R$ -176.004,28) e Harmonia (R$ -100.000,00). O aplicativo usa a base
detalhada como fonte operacional porque ela preserva as 658 movimentações e
permite que as medidas respondam aos filtros. O ranking permanece como fonte
de conciliação.

## Valores de controle

| Seleção | Créditos | Ajustes | Líquido | R$/pessoa | Espera |
|---|---:|---:|---:|---:|---:|
| Porto Alegre | R$ 16.247.674,42 | R$ -10.465.116,28 | R$ 5.782.558,14 | R$ 4,16 | 84 dias |
| Canoas | R$ 5.782.558,14 | R$ 0,00 | R$ 5.782.558,14 | R$ 16,08 | 57 dias |
| Porto Alegre + Canoas | — | — | R$ 11.565.116,28 | R$ 6,61 | — |

Para a seleção conjunta, o denominador esperado é 1.748.876 pessoas. Esse
caso confirma que o aplicativo divide os totais agregados, em vez de somar os
valores por pessoa dos dois municípios.
