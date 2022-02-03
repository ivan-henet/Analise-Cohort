import csv

import pandas as pd

def cria_tabela_cohort():

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
    vendas_ano = {}
    index_can = []
    # ----------------------------------Cria dict com somatorio de vendas anual por mês
    consulta_total_vendas = csv.DictReader(open('./progressao_agrupada.csv', encoding='utf-8'))
    for planos in consulta_total_vendas:
        if planos['data_lan'] not in vendas_ano:
            vendas_ano[f"{planos['data_lan']}"] = int(planos['total_venda'])
        if planos['data_can'] not in index_can:
            index_can.append(planos['data_can'])


    def calculos(data, tabela):
        """Subtrai do valor total vendido no ano os respectivos valores mensais
        Ex: Total Vendido Jan: 2.000
            Total Cancelado Jan: 60.00; Fev:20; Abri: 5...
            Calculo: 2000-60=1940/2000; 1940-20=1920/2000; 1920-5=1915/2000...
        """
        if str(dados['data_lan']) == data:
            vendas_ano[f'{data}'] -= int(dados['total_can'])
            mes = round(vendas_ano[f'{data}'] / int(dados['total_venda']) * 100, 2)
            tabela.append(mes)


    # ----------------------------------Cria lista com os respectivos vlores de cancelamentos e lancamentos para cada mês
    result_consultas = csv.DictReader(open('./progressao_agrupada.csv', encoding='utf-8'))
    for dados in result_consultas:
        calculos('2021-01-01', Jan)
        calculos('2021-02-01', Fev)
        calculos('2021-03-01', Mar)
        calculos('2021-04-01', Abr)
        calculos('2021-05-01', Mai)
        calculos('2021-06-01', Jun)
        calculos('2021-07-01', Jul)
        calculos('2021-08-01', Ago)
        calculos('2021-09-01', Set)
        calculos('2021-10-01', Out)
        calculos('2021-11-01', Nov)
        calculos('2021-12-01', Dez)


    def addIndex(arr, pos):
        """Cria a matriz"""
        try:
            return arr[pos]
        except:
            return 0


    # Cria a matriz 12xn
    Fev = [addIndex(Fev, i) for i in range(len(Jan))]
    Mar = [addIndex(Mar, i) for i in range(len(Jan))]
    Abr = [addIndex(Abr, i) for i in range(len(Jan))]
    Mai = [addIndex(Mai, i) for i in range(len(Jan))]
    Jun = [addIndex(Jun, i) for i in range(len(Jan))]
    Jul = [addIndex(Jul, i) for i in range(len(Jan))]
    Ago = [addIndex(Ago, i) for i in range(len(Jan))]
    Set = [addIndex(Set, i) for i in range(len(Jan))]
    Out = [addIndex(Out, i) for i in range(len(Jan))]
    Nov = [addIndex(Nov, i) for i in range(len(Jan))]
    Dez = [addIndex(Dez, i) for i in range(len(Jan))]

    full = [[Jan[i], Fev[i], Mar[i], Abr[i], Mai[i], Jun[i], Jul[i], Ago[i], Set[i], Out[i], Nov[i], Dez[i]] for i in
            range(len(Jan))]

    # ----------------------------------Atribui chaves ao valores da matriz.
    grafico = []
    for x in full:
        grafico.append(dict(jan=x[0], fev=x[1], mar=x[2], abr=x[3], mai=x[4], jun=x[5],
                            jul=x[6], ago=x[7], set=x[8], out=x[9], nov=x[10], dez=x[11],
                            ))

    # ---------------------------------- Cria a coluna de Médias.

    meses = []
    for mes in full:
        me = []
        for pos in mes:
            if pos > 0:
                me.append(pos)
        meses.append(me)

    idx_media = [len(x) for x in meses]
    medias = [sum(full[pos]) for pos in range(len(full))]

    full_medias = [(pos[0] / pos[1]) for pos in zip(medias, idx_media)]

    # ---------------------------------- Cria a coluna de churn.
    churn = []
    for pos in range(len(full_medias) - 1):
        churn.append(round(full_medias[pos + 1] - full_medias[pos], 2))
    churn.append(0)

    # ----------------------------------Prepara os dados para gerar o arquivo final de  output
    df_index_can = pd.DataFrame(index_can, columns=['index'])
    df_grafico = pd.DataFrame(grafico)
    df_medias = pd.DataFrame(full_medias, columns=['medias'])
    df_churn = pd.DataFrame(churn, columns=['churn'])
    df = pd.concat([df_index_can,df_grafico, df_medias, df_churn], axis=1)

    arquivo_csv = df.to_csv('./tabela_cohort.csv', encoding='utf-8', sep=',', index=False)

if __name__ == '__main__':
    ...