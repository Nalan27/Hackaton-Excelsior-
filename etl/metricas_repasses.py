"""Cálculos municipais derivados dos repasses do FUNDEC/RS."""

import pandas as pd


COLUNAS_FATO = {'chave_municipal', 'data', 'valor'}
COLUNAS_MARCOS = {
    'chave_municipal',
    'data_marco_adotado',
    'tipo_marco_adotado',
    'fonte_marco_adotado',
}


def _exige_colunas(df, colunas, nome):
    ausentes = sorted(colunas - set(df.columns))
    if ausentes:
        raise ValueError(f'Colunas ausentes em {nome}: {", ".join(ausentes)}')


def calcular_intervalo_primeiro_repasse(fato_repasses, marcos_temporais):
    """Calcula o intervalo entre um marco documentado e o primeiro crédito.

    Um repasse é elegível para iniciar o atendimento somente quando ``valor > 0``.
    Estornos e ajustes negativos continuam na tabela fato, mas são ignorados na
    seleção da primeira data. Intervalos negativos não são publicados como
    medida: recebem status próprio e valor nulo.
    """
    _exige_colunas(fato_repasses, COLUNAS_FATO, 'fato_repasses')
    _exige_colunas(marcos_temporais, COLUNAS_MARCOS, 'marcos_temporais')

    fato = fato_repasses.copy()
    marcos = marcos_temporais.copy()

    fato['chave_municipal'] = fato['chave_municipal'].astype('string')
    fato['data'] = pd.to_datetime(fato['data'], errors='coerce')
    fato['valor'] = pd.to_numeric(fato['valor'], errors='coerce')
    marcos['chave_municipal'] = marcos['chave_municipal'].astype('string')
    marcos['data_marco_adotado'] = pd.to_datetime(
        marcos['data_marco_adotado'], errors='coerce'
    )

    if marcos['chave_municipal'].duplicated().any():
        raise ValueError('marcos_temporais possui chave_municipal duplicada')

    creditos = fato[
        fato['chave_municipal'].notna()
        & fato['data'].notna()
        & fato['valor'].gt(0)
    ]
    primeira_data = (
        creditos.groupby('chave_municipal', as_index=False)['data']
        .min()
        .rename(columns={'data': 'data_primeiro_repasse_elegivel'})
    )

    estornos = (
        fato[fato['valor'].lt(0) & fato['chave_municipal'].notna()]
        .groupby('chave_municipal')
        .size()
        .rename('qtd_estornos_ignorados')
        .reset_index()
    )

    resultado = marcos.merge(primeira_data, on='chave_municipal', how='left')
    resultado = resultado.merge(estornos, on='chave_municipal', how='left')
    resultado['qtd_estornos_ignorados'] = (
        resultado['qtd_estornos_ignorados'].fillna(0).astype(int)
    )
    resultado['criterio_primeiro_repasse'] = 'valor > 0 e data válida'

    intervalo_bruto = (
        resultado['data_primeiro_repasse_elegivel']
        - resultado['data_marco_adotado']
    ).dt.days

    resultado['status_intervalo'] = 'ok'
    resultado.loc[
        resultado['data_marco_adotado'].isna(), 'status_intervalo'
    ] = 'sem_data_marco'
    resultado.loc[
        resultado['data_marco_adotado'].notna()
        & resultado['data_primeiro_repasse_elegivel'].isna(),
        'status_intervalo',
    ] = 'sem_primeiro_repasse_elegivel'
    resultado.loc[
        intervalo_bruto.lt(0), 'status_intervalo'
    ] = 'intervalo_negativo'

    resultado['intervalo_desde_marco_adotado_dias'] = intervalo_bruto.where(
        resultado['status_intervalo'].eq('ok')
    ).astype('Int64')

    return resultado[[
        'chave_municipal',
        'data_marco_adotado',
        'tipo_marco_adotado',
        'fonte_marco_adotado',
        'data_primeiro_repasse_elegivel',
        'intervalo_desde_marco_adotado_dias',
        'status_intervalo',
        'criterio_primeiro_repasse',
        'qtd_estornos_ignorados',
    ]]
