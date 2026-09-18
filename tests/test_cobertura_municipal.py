import csv
import unittest
from decimal import Decimal
from pathlib import Path

from etl.cobertura_municipal import (
    classificar_base,
    ler_lista_afetados,
    ler_municipios_rs,
    normalizar_nome,
)


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data/processed"


def ler_csv(nome):
    with (PROCESSED / nome).open(encoding="utf-8", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


class CoberturaMunicipalTest(unittest.TestCase):
    def test_fonte_oficial_e_conciliacao_ibge(self):
        itens = ler_lista_afetados()
        cadastro = ler_municipios_rs()
        self.assertEqual(len(itens), 478)
        self.assertEqual([ordem for ordem, _ in itens], list(range(1, 479)))
        self.assertEqual(len(cadastro), 497)
        self.assertTrue(all(normalizar_nome(nome) in cadastro for _, nome in itens))
        self.assertEqual(cadastro[normalizar_nome("Santana do Livramento")][0], "4317103")

    def test_cobertura_resultante_e_casos(self):
        cobertura = ler_csv("cobertura_municipal.csv")
        casos = ler_csv("casos_cobertura_investigacao.csv")
        fato = ler_csv("fato_repasses.csv")
        por_codigo = {linha["chave_municipal"]: linha for linha in cobertura}
        codigos_fato = {linha["chave_municipal"] for linha in fato}
        codigos_afetados = {
            linha["chave_municipal"] for linha in cobertura
            if linha["afetado_lista_2024_06_11"] == "1"
        }
        self.assertEqual(len(cobertura), 497)
        self.assertEqual(len(por_codigo), 497)
        self.assertEqual(len(codigos_afetados), 478)
        self.assertEqual(len(codigos_fato), 334)
        self.assertEqual(codigos_fato - codigos_afetados, set())
        self.assertEqual(len(codigos_afetados - codigos_fato), 144)
        self.assertEqual(sum(
            linha["chave_municipal"] in codigos_afetados
            and int(linha["qtd_movimentacoes_ate_extrato"]) > 0
            for linha in cobertura
        ), 237)
        self.assertEqual(sum(
            linha["situacao_comparacao"] == "nao_listado_sem_registro"
            for linha in cobertura
        ), 19)
        self.assertEqual(
            {linha["chave_municipal"] for linha in casos},
            codigos_afetados - codigos_fato,
        )
        self.assertEqual(sum(Decimal(linha["saldo_liquido_base"]) for linha in cobertura),
                         sum(Decimal(linha["valor"]) for linha in fato))
        self.assertEqual(por_codigo["4300034"]["situacao_na_base"], "sem_registro")
        self.assertEqual(por_codigo["4300109"]["situacao_na_base"], "saldo_positivo")

    def test_saldo_zero_nao_e_ausencia_de_registro(self):
        self.assertEqual(classificar_base(0, Decimal("0")), "sem_registro")
        self.assertEqual(classificar_base(2, Decimal("0")), "saldo_zero")
        self.assertEqual(classificar_base(1, Decimal("-1")), "saldo_negativo")


if __name__ == "__main__":
    unittest.main()
