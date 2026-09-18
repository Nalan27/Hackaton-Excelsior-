"""Compara a lista da Defesa Civil de 11/06/2024 com a base FUNDEC versionada.

A lista registra municípios afetados naquela data. Ela não é uma lista de
elegibilidade ao FUNDEC e a ausência de movimentação não prova falta de ajuda.
"""

import csv
import re
import unicodedata
from collections import defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "data/raw/pdf/defesa-civil-rs-municipios-afetados-2024-06-11.pdf"
POPULACAO = ROOT / "data/raw/csv/populacao_rs_2024.csv"
FATO = ROOT / "data/processed/fato_repasses.csv"
SAIDA = ROOT / "data/processed"
DATA_EXTRATO = date(2024, 6, 11)
PADRAO_ITEM = re.compile(r"(?m)^([^\r\n]+?)(\d{1,3})\.$")


def normalizar_nome(nome):
    texto = unicodedata.normalize("NFKD", nome.upper())
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = texto.replace("'", "").replace("’", "")
    return " ".join(texto.split())


def ler_lista_afetados(caminho=PDF):
    texto = "\n".join(pagina.extract_text() for pagina in PdfReader(caminho).pages)
    itens = [(int(ordem), nome.strip()) for nome, ordem in PADRAO_ITEM.findall(texto)]
    if [ordem for ordem, _ in itens] != list(range(1, 479)):
        raise ValueError("A extração do PDF não retornou os 478 itens em sequência")
    if len({normalizar_nome(nome) for _, nome in itens}) != 478:
        raise ValueError("Há nomes municipais duplicados na lista oficial")
    return itens


def ler_municipios_rs(caminho=POPULACAO):
    municipios = {}
    with caminho.open(encoding="utf-8-sig", newline="") as arquivo:
        for linha in csv.reader(arquivo, delimiter=";"):
            if len(linha) < 5 or linha[0] != "MU":
                continue
            codigo = linha[1].strip()
            nome = linha[2].removesuffix(" (RS)").strip()
            chave = normalizar_nome(nome)
            if len(codigo) != 7 or not codigo.startswith("43") or chave in municipios:
                raise ValueError(f"Município IBGE inválido ou duplicado: {codigo}, {nome}")
            municipios[chave] = (codigo, nome)
    if len(municipios) != 497:
        raise ValueError(f"Esperados 497 municípios do RS, encontrados {len(municipios)}")
    return municipios


def classificar_base(qtd_movimentacoes, saldo):
    if qtd_movimentacoes == 0:
        return "sem_registro"
    if saldo == 0:
        return "saldo_zero"
    return "saldo_positivo" if saldo > 0 else "saldo_negativo"


def escrever_csv(caminho, linhas, campos):
    with caminho.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos, lineterminator="\n")
        escritor.writeheader()
        escritor.writerows(linhas)


def gerar_cobertura():
    municipios = ler_municipios_rs()
    afetados = []
    for ordem, nome_fonte in ler_lista_afetados():
        chave_nome = normalizar_nome(nome_fonte)
        if chave_nome not in municipios:
            raise ValueError(f"Nome da Defesa Civil sem código IBGE: {nome_fonte}")
        codigo, nome_ibge = municipios[chave_nome]
        afetados.append({
            "ordem_fonte": ordem,
            "chave_municipal": codigo,
            "municipio_fonte": nome_fonte,
            "municipio_ibge": nome_ibge,
            "data_extrato": DATA_EXTRATO.isoformat(),
        })
    codigos_afetados = {linha["chave_municipal"] for linha in afetados}
    if len(codigos_afetados) != 478:
        raise ValueError("Códigos IBGE duplicados na lista da Defesa Civil")

    por_municipio = defaultdict(lambda: {
        "qtd": 0, "saldo": Decimal("0"), "creditos": Decimal("0"),
        "ajustes": Decimal("0"), "qtd_ate_extrato": 0,
        "saldo_ate_extrato": Decimal("0"),
    })
    datas = []
    with FATO.open(encoding="utf-8-sig", newline="") as arquivo:
        for linha in csv.DictReader(arquivo):
            codigo = linha["chave_municipal"].strip()
            data = date.fromisoformat(linha["data"])
            valor = Decimal(linha["valor"])
            datas.append(data)
            grupo = por_municipio[codigo]
            grupo["qtd"] += 1
            grupo["saldo"] += valor
            if valor > 0:
                grupo["creditos"] += valor
            elif valor < 0:
                grupo["ajustes"] += valor
            if data <= DATA_EXTRATO:
                grupo["qtd_ate_extrato"] += 1
                grupo["saldo_ate_extrato"] += valor

    codigos_rs = {codigo for codigo, _ in municipios.values()}
    desconhecidos = set(por_municipio) - codigos_rs
    if desconhecidos:
        raise ValueError(f"Repasses sem código IBGE do RS: {sorted(desconhecidos)}")
    if not datas:
        raise ValueError("A tabela fato está vazia")
    codigos_com_movimentacao = set(por_municipio)

    cobertura = []
    casos = []
    for codigo, nome in sorted(municipios.values(), key=lambda item: item[1]):
        grupo = por_municipio[codigo]
        afetado = codigo in codigos_afetados
        situacao = classificar_base(grupo["qtd"], grupo["saldo"])
        if afetado and grupo["qtd"] == 0:
            comparacao = "afetado_sem_registro"
        elif not afetado and grupo["qtd"] > 0:
            comparacao = "nao_listado_com_registro"
        elif afetado:
            comparacao = "afetado_com_registro"
        else:
            comparacao = "nao_listado_sem_registro"
        linha = {
            "chave_municipal": codigo,
            "municipio_cobertura": nome,
            "localizacao_cobertura": f"{nome}, Rio Grande do Sul, Brasil",
            "afetado_lista_2024_06_11": int(afetado),
            "qtd_movimentacoes_base": grupo["qtd"],
            "creditos_base": f"{grupo['creditos']:.2f}",
            "ajustes_negativos_base": f"{grupo['ajustes']:.2f}",
            "saldo_liquido_base": f"{grupo['saldo']:.2f}",
            "qtd_movimentacoes_ate_extrato": grupo["qtd_ate_extrato"],
            "saldo_liquido_ate_extrato": f"{grupo['saldo_ate_extrato']:.2f}",
            "situacao_na_base": situacao,
            "situacao_comparacao": comparacao,
        }
        cobertura.append(linha)
        motivos = []
        if comparacao == "afetado_sem_registro":
            motivos.append("afetado_sem_registro")
        if comparacao == "nao_listado_com_registro":
            motivos.append("nao_listado_com_registro")
        if situacao == "saldo_zero":
            motivos.append("saldo_zero_com_movimentacao")
        if motivos:
            casos.append({**linha, "motivos_investigacao": "|".join(motivos)})

    campos_cobertura = list(cobertura[0])
    escrever_csv(SAIDA / "municipios_afetados_defesa_civil_2024_06_11.csv", afetados, list(afetados[0]))
    escrever_csv(SAIDA / "cobertura_municipal.csv", cobertura, campos_cobertura)
    escrever_csv(SAIDA / "casos_cobertura_investigacao.csv", casos, campos_cobertura + ["motivos_investigacao"])

    metricas = {
        "data_extrato_lista": DATA_EXTRATO.isoformat(),
        "inicio_base_repasses": min(datas).isoformat(),
        "fim_base_repasses": max(datas).isoformat(),
        "movimentacoes_base": len(datas),
        "saldo_total_base": f"{sum((grupo['saldo'] for grupo in por_municipio.values()), Decimal('0')):.2f}",
        "municipios_rs": len(cobertura),
        "municipios_lista_afetados": len(codigos_afetados),
        "municipios_com_movimentacao": len(codigos_com_movimentacao),
        "afetados_com_movimentacao": sum(r["situacao_comparacao"] == "afetado_com_registro" for r in cobertura),
        "afetados_sem_movimentacao": sum(r["situacao_comparacao"] == "afetado_sem_registro" for r in cobertura),
        "afetados_com_movimentacao_ate_extrato": sum(
            r["afetado_lista_2024_06_11"] == 1 and r["qtd_movimentacoes_ate_extrato"] > 0
            for r in cobertura
        ),
        "nao_listados_com_movimentacao": sum(r["situacao_comparacao"] == "nao_listado_com_registro" for r in cobertura),
        "nao_listados_sem_movimentacao": sum(r["situacao_comparacao"] == "nao_listado_sem_registro" for r in cobertura),
        "saldo_zero_com_movimentacao": sum(r["situacao_na_base"] == "saldo_zero" for r in cobertura),
        "casos_para_investigacao": len(casos),
    }
    escrever_csv(SAIDA / "relatorio_cobertura.csv", [
        {"metrica": metrica, "valor": valor} for metrica, valor in metricas.items()
    ], ["metrica", "valor"])
    return metricas


if __name__ == "__main__":
    for chave, valor in gerar_cobertura().items():
        print(f"{chave}: {valor}")
