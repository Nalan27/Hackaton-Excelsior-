"""Resume a associação descritiva entre IDH-M 2010 e FUNDEC por pessoa em 2024."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def analisar() -> dict:
    municipios = pd.read_csv(
        PROCESSED / "dim_municipio.csv",
        dtype={"chave_municipal": str, "codigo_ibge": str},
    )
    repasses = pd.read_csv(PROCESSED / "fato_repasses.csv")

    if municipios["codigo_ibge"].isna().any() or municipios["codigo_ibge"].duplicated().any():
        raise ValueError("Cada município precisa de um código IBGE único.")
    if municipios["populacao_2024"].isna().any() or (municipios["populacao_2024"] <= 0).any():
        raise ValueError("População 2024 ausente ou não positiva.")
    if municipios["total_repasses"].isna().any():
        raise ValueError("Saldo líquido municipal ausente.")

    total_municipal = municipios["total_repasses"].sum()
    total_fato = repasses["valor"].sum()
    if abs(total_municipal - total_fato) > 0.01:
        raise ValueError("Soma dos municípios diverge da tabela fato.")

    municipios["reais_por_pessoa"] = (
        municipios["total_repasses"] / municipios["populacao_2024"]
    )
    if not municipios["reais_por_pessoa"].round(8).equals(
        municipios["valor_por_pessoa_2024"].round(8)
    ):
        raise ValueError("Indicador por pessoa diverge da razão entre saldo e população.")

    sem_idhm = municipios.loc[
        municipios["idhm_2010"].isna(),
        ["codigo_ibge", "municipio_ibge_2024"],
    ]
    validos = municipios.dropna(subset=["idhm_2010"]).copy()
    if validos.empty:
        raise ValueError("Nenhum município tem IDH-M para comparação.")

    limites = validos["idhm_2010"].quantile([0.25, 0.5, 0.75])
    validos["faixa_idhm"] = pd.cut(
        validos["idhm_2010"],
        bins=[float("-inf"), *limites.tolist(), float("inf")],
        labels=["Q1", "Q2", "Q3", "Q4"],
    )

    grupos = []
    for faixa, grupo in validos.groupby("faixa_idhm", observed=True):
        grupos.append(
            {
                "faixa": str(faixa),
                "municipios": int(len(grupo)),
                "idhm_min": float(grupo["idhm_2010"].min()),
                "idhm_max": float(grupo["idhm_2010"].max()),
                "mediana_reais_por_pessoa": round(float(grupo["reais_por_pessoa"].median()), 2),
                "media_reais_por_pessoa": round(float(grupo["reais_por_pessoa"].mean()), 2),
            }
        )

    populacao_minima = 5000
    maiores = validos.loc[validos["populacao_2024"] >= populacao_minima]

    def correlacoes(tabela: pd.DataFrame) -> dict:
        idhm = tabela["idhm_2010"]
        repasse = tabela["reais_por_pessoa"]
        return {
            "pearson": round(float(idhm.corr(repasse)), 4),
            "spearman": round(float(idhm.rank().corr(repasse.rank())), 4),
        }

    return {
        "periodo_repasses": [str(repasses["data"].min()), str(repasses["data"].max())],
        "ano_idhm": 2010,
        "ano_populacao": 2024,
        "municipios_com_repasses": int(len(municipios)),
        "municipios_comparaveis": int(len(validos)),
        "sem_idhm": sem_idhm.to_dict("records"),
        "saldo_liquido_total": round(float(total_municipal), 2),
        "correlacoes": correlacoes(validos),
        "limites_quartis_idhm": [round(float(valor), 3) for valor in limites],
        "faixas_idhm": grupos,
        "sensibilidade_populacao": {
            "minimo_pessoas": populacao_minima,
            "municipios": int(len(maiores)),
            "correlacoes": correlacoes(maiores),
        },
    }


if __name__ == "__main__":
    print(json.dumps(analisar(), ensure_ascii=False, indent=2))
