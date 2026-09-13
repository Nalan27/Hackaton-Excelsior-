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
        cls.intervalos = read_csv('intervalo_primeiro_repasse.csv')
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
        campos_intervalos = set(self.intervalos[0])
        self.assertEqual(campos_fato & campos_municipio, {'chave_municipal'})
        self.assertEqual(campos_fato & campos_calendario, {'data'})
        self.assertEqual(campos_municipio & campos_calendario, set())
        self.assertEqual(campos_fato & campos_intervalos, {'chave_municipal'})
        self.assertEqual(campos_municipio & campos_intervalos, {'chave_municipal'})
        self.assertEqual(campos_calendario & campos_intervalos, set())

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

            fks_intervalos = conn.execute(
                'PRAGMA foreign_key_list(intervalo_primeiro_repasse)'
            ).fetchall()
            referencias_intervalos = {
                (fk[2], fk[3], fk[4]) for fk in fks_intervalos
            }
            self.assertEqual(referencias_intervalos, {
                ('dim_municipio', 'chave_municipal', 'chave_municipal'),
            })

    def test_script_qlik_usa_sintaxe_csv_valida(self):
        script = (ROOT / 'qlik' / 'load_data.qvs').read_text(encoding='utf-8')
        self.assertEqual(script.count("(utf8, txt, embedded labels, delimiter is ',', msq);"), 4)
        self.assertNotIn('CsvSimple', script)

    def test_intervalo_usa_primeiro_credito_e_marco_documentado(self):
        self.assertEqual(len(self.intervalos), 334)
        self.assertEqual(
            {row['status_intervalo'] for row in self.intervalos},
            {'ok'},
        )
        self.assertEqual(
            {row['data_marco_adotado'] for row in self.intervalos},
            {'2024-04-24'},
        )
        self.assertEqual(
            {row['criterio_primeiro_repasse'] for row in self.intervalos},
            {'valor > 0 e data válida'},
        )

        primeiras_datas = [
            datetime.strptime(row['data_primeiro_repasse_elegivel'], '%Y-%m-%d').date()
            for row in self.intervalos
        ]
        intervalos = [
            int(row['intervalo_desde_marco_adotado_dias'])
            for row in self.intervalos
        ]
        self.assertEqual(min(primeiras_datas).isoformat(), '2024-05-17')
        self.assertEqual(max(primeiras_datas).isoformat(), '2024-09-06')
        self.assertEqual(min(intervalos), 23)
        self.assertEqual(max(intervalos), 135)
        self.assertEqual(
            sum(int(row['qtd_estornos_ignorados']) for row in self.intervalos),
            18,
        )

    def test_calendario_e_continuo_e_cobre_a_fato(self):
        datas_calendario = [
            datetime.strptime(row['data'], '%Y-%m-%d').date()
            for row in self.calendario
        ]
        datas_fato = {
            datetime.strptime(row['data'], '%Y-%m-%d').date()
            for row in self.fato
        }

        # O período de 17/05/2024 até 26/09/2024 possui 133 dias.
        self.assertEqual(len(datas_calendario), 133)

        # Não pode haver datas duplicadas.
        self.assertEqual(
            len(datas_calendario),
            len(set(datas_calendario)),
        )

        # Todas as datas da fato devem existir no calendário.
        self.assertTrue(datas_fato <= set(datas_calendario))

        # Confirma os limites do calendário.
        self.assertEqual(
            datas_calendario[0].isoformat(),
            '2024-05-17',
        )
        self.assertEqual(
            datas_calendario[-1].isoformat(),
            '2024-09-26',
        )

        # Confirma que não existem dias faltando.
        for anterior, seguinte in zip(
            datas_calendario,
            datas_calendario[1:],
        ):
            self.assertEqual((seguinte - anterior).days, 1)

    def test_atributos_do_calendario(self):
        calendario_por_data = {
            row['data']: row
            for row in self.calendario
        }

        maio = calendario_por_data['2024-05-17']
        self.assertEqual(maio['ano'], '2024')
        self.assertEqual(maio['trimestre'], 'T2')
        self.assertEqual(maio['mes'], '5')
        self.assertEqual(maio['mes_nome'], 'Maio')
        self.assertEqual(maio['ano_mes'], '2024-05')
        self.assertEqual(maio['ano_mes_ordem'], '202405')

        setembro = calendario_por_data['2024-09-26']
        self.assertEqual(setembro['ano'], '2024')
        self.assertEqual(setembro['trimestre'], 'T3')
        self.assertEqual(setembro['mes'], '9')
        self.assertEqual(setembro['mes_nome'], 'Setembro')
        self.assertEqual(setembro['ano_mes'], '2024-09')
        self.assertEqual(setembro['ano_mes_ordem'], '202409')
if __name__ == '__main__':
    unittest.main()
