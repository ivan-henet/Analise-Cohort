import pandas as pd

from appV1.extracao.query import consulta_ocorrencias_progressao


def cria_tabela_cohort():

    result_consulta = consulta_ocorrencias_progressao()

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

    total_vendido = {}

    def calculos(data, tabela):
        """ Subtrai os cancelamentos jan/dez do total vendido no mes base."""

        if str(dados[0]) == data:
            total_vendido[f'{data}'] -= int(dados[3])
            mes = round(total_vendido[f'{data}'] / int(dados[1]) * 100, 2)
            tabela.append(mes)

    for planos in result_consulta:
        if planos[0] not in total_vendido:
            total_vendido[f'{planos[0]}'] = planos[1]

    for dados in result_consulta:
        calculos('2021-01', Jan)
        calculos('2021-02', Fev)
        calculos('2021-03', Mar)
        calculos('2021-04', Abr)
        calculos('2021-05', Mai)
        calculos('2021-06', Jun)
        calculos('2021-07', Jul)
        calculos('2021-08', Ago)
        calculos('2021-09', Set)
        calculos('2021-10', Out)
        calculos('2021-11', Nov)
        calculos('2021-12', Dez)

    i = 0
    top = []

    def addIndex(arr, pos):
        try:
            return arr[pos]
        except:
            return 0

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

    grafico = []
    for x in full:
        grafico.append(dict(jan=x[0], fev=x[1], mar=x[2], abr=x[3], mai=x[4], jun=x[5],
                            jul=x[6], ago=x[7], set=x[8], out=x[9], nov=x[10], dez=x[11],
                            ))

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

    churn = []
    for pos in range(len(full_medias) - 1):
        churn.append(round(full_medias[pos + 1] - full_medias[pos], 2))
    churn.append(0)

    df_grafico = pd.DataFrame(grafico)
    df_medias = pd.DataFrame(full_medias, columns=['medias'])
    df_churn = pd.DataFrame(churn, columns=['churn'])
    df = pd.concat([df_grafico, df_medias, df_churn], axis=1)
    arquivo_csv = df.to_csv('tabela_cohort.csv', encoding='utf-8', sep=',')

