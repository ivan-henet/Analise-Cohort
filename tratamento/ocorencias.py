import csv
import itertools
from collections import Counter, defaultdict
from datetime import datetime as dt
from typing import DefaultDict

import numpy as np
import pandas as pd

from extracao.query import consulta_vendidos_e_cancelados

#result = csv.DictReader(open('progressao.csv', encoding='utf-8'))


class Cohort:
    def __init__(self, inicio, fim):

        self.fim = fim
        self.inicio = inicio
        self.lista_cadastrados = []
        self.tabela_ocorrencias = []
        self.qtd_cancelados = []
        self.grupo_cancelado = []

    def trata_datas(self):
        """ Extrai ano e mes das respectivas datas"""
        results = consulta_vendidos_e_cancelados(self.inicio, self.fim)

        for dados in results:
            codsercli = dados[1]
            data_lan = dados[2]

            if dados[4] == '0000-00-00':
                data_can = dt(year=1, month=1, day=1)
            else:
                data_can = dt.strptime(dados[4], '%Y-%m-%d')
            # data_lan = dt.strptime(dados['data_lan'], '%Y-%m-%d').date()
            # data_can = dt.strptime(dados['data_can'], '%Y-%m-%d').date()

            mes_ano_cadastro = dt(data_lan.year, data_lan.month, 1).date()
            mes_ano_can = dt(data_can.year, data_can.month, 1).date()

            self.lista_cadastrados.append((codsercli, mes_ano_cadastro, mes_ano_can))

    def agrupa_por_mes(self):
        """Ordena os dados e e agrupa por data de cadastro"""

        ordem_lista = sorted(self.lista_cadastrados)
        for _, v in itertools.groupby(ordem_lista, key=lambda x: x[1]):
            self.grupo_cancelado.append(list(v))

    def cria_tabela(self):
        """ Cria conta as ocorrencias de cancelamento para cada mes de cadastro"""

        for lista in self.grupo_cancelado:
            grupos = Counter(lista).most_common()

            for dados in grupos:
                mes, qtd_can = dados

                self.tabela_ocorrencias.append(
                    dict(codsercli=mes[0], mes_cadastro=mes[1],
                         mes_can=mes[2], qtd_can=qtd_can))
                self.qtd_cancelados.append(qtd_can)

    def gera_arquivo_csv(self):
        ...
        #arquivo_csv = pd.DataFrame(self.tabela_ocorrencias)
       # arquivo_csv.to_csv('./tabela_ocorrencias.csv', sep=',', encoding='utf-8')


if __name__ == '__main__':
    cohort = Cohort('2021-01-01', '2021-12-31')
    cohort.trata_datas()
    cohort.agrupa_por_mes()
    cohort.cria_tabela()
    cohort.gera_arquivo_csv()





    # def calcula_churn(self):
    #     for pos in range(len(self.qtd_cancelados) - 1):
    #         self.churn.append(dict(churn=self.qtd_cancelados[pos + 1] - self.qtd_cancelados[pos]))

    # def calcula_ocorrencias_por_mes(self):
    #     df_cohort = pd.DataFrame(self.tabela_cohort)
    #
    #     grupo = df_cohort.groupby(['mes_cadastro', 'mes_can', 'qtd_vendidos'])
    #     self.cohorts = grupo.agg({'codsercli': pd.Series.nunique, 'qtd_can': sum})
    #
    #     return self.cohorts

    # def calcula_dif_periodos(sefl, df):
    #     df['index_delta'] = np.arange(len(df)) + 1
    #     return df
    #
    # def cria_tabela_retencao(self):
    #     cohorts = self.cohorts.groupby(level='mes_cadastro').apply(self.calcula_dif_periodos).reset_index()
    #     cohorts = cohorts.set_index(['mes_cadastro', 'index_delta'])
    #     #primeiro_valor = cohorts.iloc[:1, 1] - cohorts.iloc[:1, 3]
    #     cohorts['dif_%'] = cohorts.iloc[:1, 1] - cohorts.iloc[:1, 3]

    # cohorts['churn'] = (cohorts['dif_%'] - cohorts['dif_%'].shift(1)) / cohorts['qtd_vendidos']*100

    # cohorts['dif_%'] = (cohorts['codsercli'] - cohorts['qtd_vendidos']) / cohorts['qtd_vendidos']
    # print(cohorts)

    # cc = cohorts.pivot_table(index='mes_cadastro', columns='index_delta', values='codsercli')

    # cs = cc.iloc[:, 0]
    # self.matrix_retencao = cc.divide(cs, axis=0)
    # print(self.matrix_retencao)
    # return self.matrix_retencao

    # cohorts_size = cohorts['codsercli'].groupby(level='mes_cadastro').first()
    ##.user_retention = (cohorts['qtd_can'].unstack('mes_cadastro').divide(cohorts_size, axis=1))
    # print(self.user_retention)
    # return round(self.user_retention, 2)*100