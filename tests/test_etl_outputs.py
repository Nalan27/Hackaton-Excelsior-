import csv
import sqlite3
import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / 'data' / 'processed'
RAW = ROOT / 'data' / 'raw' / 'csv'


def read_csv(name):
    with (PROCESSED / name).open(encoding='utf-8', newline='') as arquivo:
        return list(csv.DictReader(arquivo))


def read_raw_csv(name):
    with (RAW / name).open(encoding='utf-8', newline='') as arquivo:
        return list(csv.DictReader(arquivo))


class EtlOutputsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fato = read_csv('fato_repasses.csv')
        cls.municipios = read_csv('dim_municipio.csv')
        cls.calendario = read_csv('dim_calendario.csv')
        cls.conciliacao = read_csv('conciliacao.csv')
        cls.inconsistencias = read_csv('inconsistencias.csv')
        cls.validacao = read_csv('relatorio_validacao.csv')
        cls.repasses_origem = read_raw_csv('repasses_fundec_2024.csv')

    def test_quantidades_e_tipos_criticos(self):
        self.assertEqual(len(self.fato), 658)
        self.assertEqual(len(self.municipios), 334)
        self.assertTrue(all(row['valor'] for row in self.fato))
        self.assertTrue(all(
            datetime.strptime(row['data'], '%Y-%m-%d') for row in self.fato
        ))

    def test_valores_negativos_e_totais(self):
        valores = [Decimal(row['valor']) for row in self.fato]
        negativos = [valor for valor in valores if valor < 0]
        self.assertEqual(len(negativos), 18)
        self.assertEqual(sum(negativos), Decimal('-18634883.72'))
        self.assertEqual(sum(valores), Decimal('288699999.97'))

    def test_identificadores_textuais_foram_preservados(self):
        self.assertEqual(len(self.repasses_origem), len(self.fato))
        for origem, tratado in zip(self.repasses_origem, self.fato):
            self.assertEqual(origem['Processo'], tratado['processo'])
            self.assertEqual(origem['Empenho'], tratado['empenho'])
            self.assertEqual(origem['CNPJ'], tratado['cnpj'])

    def test_chaves_municipais_integras(self):
        chaves_dim = {row['chave_municipal'] for row in self.municipios}
        chaves_fato = {row['chave_municipal'] for row in self.fato}
        self.assertEqual(len(chaves_dim), 334)
        self.assertTrue(all(len(chave) == 7 and chave.isdigit() for chave in chaves_dim))
        self.assertTrue(chaves_fato <= chaves_dim)
        self.assertNotIn('', chaves_fato)

    def test_modelo_nao_cria_chaves_sinteticas(self):
        campos_fato = set(self.fato[0])
        campos_municipio = set(self.municipios[0])
        campos_calendario = set(self.calendario[0])
        self.assertEqual(campos_fato & campos_municipio, {'chave_municipal'})
        self.assertEqual(campos_fato & campos_calendario, {'data'})
        self.assertEqual(campos_municipio & campos_calendario, set())

    def test_conciliacao_documenta_as_tres_diferencas(self):
        divergencias = {
            row['município']: Decimal(row['diferenca'])
            for row in self.conciliacao
            if abs(Decimal(row['diferenca'])) > Decimal('0.01')
        }
        self.assertEqual(divergencias, {
            'Sao Sebastiao do Cai': Decimal('-200000.0'),
            'Canoas': Decimal('-176004.28'),
            'Harmonia': Decimal('-100000.0'),
        })

    def test_idhm_ausente_esta_documentado(self):
        avisos = [
            row for row in self.inconsistencias
            if row['severidade'] == 'AVISO' and row['tipo'] == 'indicador_ausente'
        ]
        self.assertEqual(len(avisos), 1)
        self.assertEqual(avisos[0]['municipio'], 'Pinto Bandeira')
        self.assertIn('idhm_2010', avisos[0]['detalhe'])

    def test_validacoes_criticas_passaram(self):
        erros = [row for row in self.validacao if row['status'] == 'ERRO']
        self.assertEqual(erros, [])

    def test_sqlite_declara_pk_e_fks(self):
        with sqlite3.connect(ROOT / 'banco_hackathon.db') as conn:
            colunas_dim = conn.execute('PRAGMA table_info(dim_municipio)').fetchall()
            chave = next(coluna for coluna in colunas_dim if coluna[1] == 'chave_municipal')
            self.assertEqual(chave[5], 1)

            fks = conn.execute('PRAGMA foreign_key_list(fato_repasses)').fetchall()
            referencias = {(fk[2], fk[3], fk[4]) for fk in fks}
            self.assertEqual(referencias, {
                ('dim_municipio', 'chave_municipal', 'chave_municipal'),
                ('dim_calendario', 'data', 'data'),
            })

    def test_script_qlik_usa_sintaxe_csv_valida(self):
        script = (ROOT / 'qlik' / 'load_data.qvs').read_text(encoding='utf-8')
        self.assertEqual(script.count("(utf8, txt, embedded labels, delimiter is ',', msq);"), 3)
        self.assertNotIn('CsvSimple', script)


if __name__ == '__main__':
    unittest.main()
