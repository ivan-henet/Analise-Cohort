import csv
from collections import Counter
from datetime import datetime as dt
import pandas as pd

def agrupa_tabela_progressao():
    result_progressao = csv.DictReader(open('./tabela_progressao.csv', encoding='utf-8'))

    tabela_lancados = []
    Jan = []
    Fev = []
    Mar = []
    Abr = []
    Mai = []
    Jun = []
    Jul = []
    Ago = []
    Set = []
    Out = []
    Nov = []
    Dez = []

    for dados in result_progressao:
        # Convertendo a string em datetime
        data_lan = dt.strptime(dados['data_lan'], '%Y-%m-%d')
        data_can = dt.strptime(dados['data_can'], '%Y-%m-%d')

        # Extraindo ano e mes das datas
        ano_mes_lan = dt(data_lan.year, data_lan.month, 1).date()
        ano_mes_can = dt(data_can.year, data_can.month, 1).date()

        # Criando a tupla com os dados necessarios
        tab = ano_mes_lan, ano_mes_can, dados['codsercli']

        # Adicionando a lista apenas os dados cancelados
        # if ano_mes_can != dt(1, 1, 1).date():  # Descarta os ativos
        tabela_lancados.append(tab)


    def addMes(mes, lista):
        opcoes = {'Jan': dt(2021, 1, 1).date(), 'Fev': dt(2021, 2, 1).date(), 'Mar': dt(2021, 3, 1).date(),
                  'Abr': dt(2021, 4, 1).date(), 'Mai': dt(2021, 5, 1).date(), 'Jun': dt(2021, 6, 1).date(),
                  'Jul': dt(2021, 7, 1).date(), 'Ago': dt(2021, 8, 1).date(), 'Set': dt(2021, 9, 1).date(),
                  'Out': dt(2021, 10, 1).date(), 'Nov': dt(2021, 11, 1).date(), 'Dez': dt(2021, 12, 1).date()}
        if tab[0] == opcoes[mes]:
            lista.append(tab)


    for tab in tabela_lancados:
        addMes('Jan', Jan)
        addMes('Fev', Fev)
        addMes('Mar', Mar)
        addMes('Abr', Abr)
        addMes('Mai', Mai)
        addMes('Jun', Jun)
        addMes('Jul', Jul)
        addMes('Ago', Ago)
        addMes('Set', Set)
        addMes('Out', Out)
        addMes('Nov', Nov)
        addMes('Dez', Dez)

    # Conta as ocorrencias de datas
    #  if i[1] != dt(1, 1, 1).date() ->> Descarta os ativos
    can_jan = Counter([i[1] for i in Jan if i[1] != dt(1, 1, 1).date()]).most_common()
    can_fev = Counter([i[1] for i in Fev if i[1] != dt(1, 1, 1).date()]).most_common()
    can_mar = Counter([i[1] for i in Mar if i[1] != dt(1, 1, 1).date()]).most_common()
    can_abr = Counter([i[1] for i in Abr if i[1] != dt(1, 1, 1).date()]).most_common()
    can_mai = Counter([i[1] for i in Mai if i[1] != dt(1, 1, 1).date()]).most_common()
    can_jun = Counter([i[1] for i in Jun if i[1] != dt(1, 1, 1).date()]).most_common()
    can_jul = Counter([i[1] for i in Jul if i[1] != dt(1, 1, 1).date()]).most_common()
    can_ago = Counter([i[1] for i in Ago if i[1] != dt(1, 1, 1).date()]).most_common()
    can_set = Counter([i[1] for i in Set if i[1] != dt(1, 1, 1).date()]).most_common()
    can_out = Counter([i[1] for i in Out if i[1] != dt(1, 1, 1).date()]).most_common()
    can_nov = Counter([i[1] for i in Nov if i[1] != dt(1, 1, 1).date()]).most_common()
    can_dez = Counter([i[1] for i in Dez if i[1] != dt(1, 1, 1).date()]).most_common()

    # Cria a tabela de resultado  Agrupando datas e quantidades
    cohort_jan = pd.DataFrame(
        [dict(data_lan=Jan[0][0], total_venda=len(Jan), data_can=j[0], total_can=j[1]) for j in can_jan])
    cohort_fev = pd.DataFrame(
        [dict(data_lan=Fev[0][0], total_venda=len(Fev), data_can=j[0], total_can=j[1]) for j in can_fev])
    cohort_mar = pd.DataFrame(
        [dict(data_lan=Mar[0][0], total_venda=len(Mar), data_can=j[0], total_can=j[1]) for j in can_mar])
    cohort_abr = pd.DataFrame(
        [dict(data_lan=Abr[0][0], total_venda=len(Abr), data_can=j[0], total_can=j[1]) for j in can_abr])
    cohort_mai = pd.DataFrame(
        [dict(data_lan=Mai[0][0], total_venda=len(Mai), data_can=j[0], total_can=j[1]) for j in can_mai])
    cohort_jun = pd.DataFrame(
        [dict(data_lan=Jun[0][0], total_venda=len(Jun), data_can=j[0], total_can=j[1]) for j in can_jun])
    cohort_jul = pd.DataFrame(
        [dict(data_lan=Jul[0][0], total_venda=len(Jul), data_can=j[0], total_can=j[1]) for j in can_jul])
    cohort_ago = pd.DataFrame(
        [dict(data_lan=Ago[0][0], total_venda=len(Ago), data_can=j[0], total_can=j[1]) for j in can_ago])
    cohort_set = pd.DataFrame(
        [dict(data_lan=Set[0][0], total_venda=len(Set), data_can=j[0], total_can=j[1]) for j in can_set])
    cohort_out = pd.DataFrame(
        [dict(data_lan=Out[0][0], total_venda=len(Out), data_can=j[0], total_can=j[1]) for j in can_out])
    cohort_nov = pd.DataFrame(
        [dict(data_lan=Nov[0][0], total_venda=len(Nov), data_can=j[0], total_can=j[1]) for j in can_nov])
    cohort_dez = pd.DataFrame(
        [dict(data_lan=Dez[0][0], total_venda=len(Dez), data_can=j[0], total_can=j[1]) for j in can_dez])

    tabela = pd.concat([cohort_jan, cohort_fev, cohort_mar, cohort_abr, cohort_mai, cohort_jun, cohort_jul,
                        cohort_ago, cohort_set, cohort_out, cohort_nov, cohort_dez], axis=0).sort_values(['data_lan','data_can'])

    tabela.to_csv('progressao_agrupada.csv', encoding='utf-8', sep=',', index=False)
