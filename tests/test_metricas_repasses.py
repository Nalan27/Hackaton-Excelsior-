import unittest

import pandas as pd

from etl.metricas_repasses import calcular_intervalo_primeiro_repasse


class MetricasRepassesTest(unittest.TestCase):
    def setUp(self):
        self.fato = pd.DataFrame([
            {'chave_municipal': 'A', 'data': '2024-05-03', 'valor': -100},
            {'chave_municipal': 'A', 'data': '2024-05-05', 'valor': 50},
            {'chave_municipal': 'B', 'data': '2024-04-30', 'valor': 10},
            {'chave_municipal': 'C', 'data': '2024-05-02', 'valor': -10},
            {'chave_municipal': 'D', 'data': None, 'valor': 10},
        ])
        self.marcos = pd.DataFrame([
            {
                'chave_municipal': chave,
                'data_marco_adotado': data,
                'tipo_marco_adotado': 'marco de teste',
                'fonte_marco_adotado': 'fonte de teste',
            }
            for chave, data in [
                ('A', '2024-05-01'),
                ('B', '2024-05-01'),
                ('C', '2024-05-01'),
                ('D', '2024-05-01'),
                ('E', None),
            ]
        ])

    def test_estorno_nao_inicia_atendimento(self):
        resultado = calcular_intervalo_primeiro_repasse(self.fato, self.marcos)
        por_chave = resultado.set_index('chave_municipal')

        self.assertEqual(
            por_chave.loc['A', 'data_primeiro_repasse_elegivel'],
            pd.Timestamp('2024-05-05'),
        )
        self.assertEqual(
            por_chave.loc['A', 'intervalo_desde_marco_adotado_dias'],
            4,
        )
        self.assertEqual(por_chave.loc['A', 'qtd_estornos_ignorados'], 1)

    def test_datas_ausentes_e_intervalo_negativo_recebem_status(self):
        resultado = calcular_intervalo_primeiro_repasse(self.fato, self.marcos)
        por_chave = resultado.set_index('chave_municipal')

        self.assertEqual(por_chave.loc['B', 'status_intervalo'], 'intervalo_negativo')
        self.assertTrue(pd.isna(
            por_chave.loc['B', 'intervalo_desde_marco_adotado_dias']
        ))
        self.assertEqual(
            por_chave.loc['C', 'status_intervalo'],
            'sem_primeiro_repasse_elegivel',
        )
        self.assertEqual(
            por_chave.loc['D', 'status_intervalo'],
            'sem_primeiro_repasse_elegivel',
        )
        self.assertEqual(por_chave.loc['E', 'status_intervalo'], 'sem_data_marco')

    def test_marco_duplicado_falha_explicitamente(self):
        marcos_duplicados = pd.concat([self.marcos, self.marcos.iloc[[0]]])
        with self.assertRaisesRegex(ValueError, 'chave_municipal duplicada'):
            calcular_intervalo_primeiro_repasse(self.fato, marcos_duplicados)


if __name__ == '__main__':
    unittest.main()
