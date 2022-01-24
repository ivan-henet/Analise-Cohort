import csv
import itertools
from collections import Counter
from datetime import datetime as dt

import numpy as np
import pandas as pd

result = csv.DictReader(open('progressao.csv', encoding='utf-8'))


class Cohort:
    def __init__(self):

        self.cohorts = None
        self.user_retention = None
        self.lista_cadastrados = []
        self.lista_cancelados = []
        self.tabela_cohort = []
        self.qtd_cancelados = []
        self.churn = []
        self.grupo_cancelado = []

    def trata_datas(self):
        for dados in result:
            if dados['data_can'] != '0001-01-01':
                data_cad = dt.strptime(dados['data_lan'], '%Y-%m-%d')
                data_can = dt.strptime(dados['data_can'], '%Y-%m-%d')
                codsercli = dados['codsercli']

                mes_ano_cadastro = dt(data_cad.year, data_cad.month, 1).date()
                mes_ano_can = dt(data_can.year, data_can.month, 1).date()

                self.lista_cadastrados.append((codsercli, mes_ano_cadastro, mes_ano_can))

    def agrupa_por_mes(self):
        ordem_lista = sorted(self.lista_cadastrados)
        for _, v in itertools.groupby(ordem_lista, key=lambda x: x[0]):
            self.grupo_cancelado.append(list(v))

    def cria_tabela(self):
        for lista in self.grupo_cancelado:
            grupos = Counter(lista).most_common()
            for dados in grupos:
                mes, qtd_can = dados
                self.tabela_cohort.append(
                    dict(codsercli=mes[0], idx_lan=mes[1].month, mes_cadastro=mes[1], idx_can=mes[2].month,
                         mes_can=mes[2], qtd_can=qtd_can))
                self.qtd_cancelados.append(qtd_can)

    def calcula_churn(self):
        for pos in range(len(self.qtd_cancelados) - 1):
            self.churn.append(dict(churn=self.qtd_cancelados[pos + 1] - self.qtd_cancelados[pos]))

    def calcula_ocorrencias_por_mes(self):

        df_cohort = pd.DataFrame(self.tabela_cohort)
        df_churn = pd.DataFrame(self.churn)
        #df_ocorrencias = pd.concat([df_cohort, df_churn], axis=1)

        grupo = df_cohort.groupby(['mes_cadastro', 'mes_can'])
        self.cohorts = grupo.agg({'codsercli': pd.Series.nunique, 'qtd_can': sum})
        return self.cohorts

    def calcula_dif_periodos(sefl, df):
        df['index_delta'] = np.arange(len(df)) + 1
        return df

    def cria_tabela_retencao(self):
        cohorts = self.cohorts.groupby(level='mes_cadastro').apply(self.calcula_dif_periodos).reset_index()
        cohorts = cohorts.set_index(['mes_cadastro', 'index_delta'])

        cc = cohorts.pivot_table(index='mes_cadastro', columns='index_delta', values = 'codsercli')
        cs = cc.iloc[:,0]
        retencao = cc.divide(cs, axis=0)
       # cohorts_size = cohorts['codsercli'].groupby(level='mes_cadastro').first()

        #self.user_retention = (cohorts['qtd_can'].unstack('mes_cadastro').divide(cohorts_size, axis=1))

        print(retencao)

       # return round(self.user_retention, 2)*100

    def gera_arquivo_csv(self):
        arquivo_csv = pd.DataFrame(self.user_retention)
        #arquivo_csv.to_csv('./tabela_retencao.csv', sep=',', encoding='utf-8')


if __name__ == '__main__':
    cohort = Cohort()
    cohort.trata_datas()
    cohort.agrupa_por_mes()
    cohort.cria_tabela()
    cohort.calcula_churn()
    cohort.calcula_ocorrencias_por_mes()
    cohort.cria_tabela_retencao()
    cohort.gera_arquivo_csv()
