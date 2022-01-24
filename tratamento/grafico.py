import csv
import pandas as pd

data = csv.DictReader(open('../result.csv', encoding='utf-8'))
data2 = csv.DictReader(open('../result2.csv', encoding='utf-8'))

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

vlr_jan = []
vlr_fev = []
vlr_mar = []
vlr_abr = []
vlr_mai = []
vlr_jun = []
vlr_jul = []
vlr_ago = []
vlr_set = []
vlr_out = []
vlr_nov = []
vlr_dez = []

valor_base = {}
dicionario = {'janeiro': 2314, 'fevereiro': 2183, 'marco': 2663, 'abril': 2376, 'maio': 4172, 'junho': 3999,
              'julho': 5024, 'agosto': 4353, 'setembro': 4056, 'outubro': 4064, 'novembro': 4304, 'dezembro': 3634}


def add_vlr_base(data, mes):
    if valor['lancamento'] == data:
        valor_base[mes] = valor['total_venda']


def calcula_percentual(mes, mes_base, tabela):
    valor_fixo = valor_base
    if row[mes] != '':
        dicionario[mes_base] -= int(row[mes])
        jan = round(dicionario[mes_base] / int(valor_fixo[mes_base]) * 100, 2)
        tabela.append(jan)


for valor in data2:
    add_vlr_base('2021-01', 'janeiro')
    add_vlr_base('2021-02', 'fevereiro')
    add_vlr_base('2021-03', 'marco')
    add_vlr_base('2021-04', 'abril')
    add_vlr_base('2021-05', 'maio')
    add_vlr_base('2021-06', 'junho')
    add_vlr_base('2021-07', 'julho')
    add_vlr_base('2021-08', 'agosto')
    add_vlr_base('2021-09', 'setembro')
    add_vlr_base('2021-10', 'outubro')
    add_vlr_base('2021-11', 'novembro')
    add_vlr_base('2021-12', 'dezembro')

for row in data:
    calcula_percentual('janeiro', 'janeiro', Jan)
    calcula_percentual('fevereiro', 'fevereiro', Fev)
    calcula_percentual('marco', 'marco', Mar)
    calcula_percentual('abril', 'abril', Abr)
    calcula_percentual('maio', 'maio', Mai)
    calcula_percentual('junho', 'junho', Jun)
    calcula_percentual('julho', 'julho', Jul)
    calcula_percentual('agosto', 'agosto', Ago)
    calcula_percentual('setembro', 'setembro', Set)
    calcula_percentual('outubro', 'outubro', Out)
    calcula_percentual('novembro', 'novembro', Nov)
    calcula_percentual('dezembro', 'dezembro', Dez)
    # if row['janeiro'] != '':
    #    jan = round((int(vlr_jan[0]) - int(row['janeiro']))/int(vlr_jan[0])*100,2)
    #    Jan.append(jan)

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

tabela = []
for x in full:
    tabela.append(dict(janeiro=x[0], fevereiro=x[1], marco=x[2], abril=x[3], maio=x[4], junho=x[5],
                       julho=x[6], agosto=x[7], setembro=x[8], outubro=x[9], novembro=x[10], dezembro=x[11],
                       ))

full_medias = [round(sum(full[0]) / 12, 2), round(sum(full[1]) / 11, 2),
               round(sum(full[2]) / 10, 2), round(sum(full[3]) / 9, 2),
               round(sum(full[4]) / 8, 2), round(sum(full[5]) / 7, 2),
               round(sum(full[6]) / 6, 2), round(sum(full[7]) / 5, 2),
               round(sum(full[8]) / 4, 2), round(sum(full[9]) / 3, 2),
               round(sum(full[10]) / 2, 2), round(sum(full[11]) / 1, 2)]


medias = []
for med in full_medias:
    medias.append(dict(medias=med))

df_tabela = pd.DataFrame(tabela)
df_medias = pd.DataFrame(medias)
df = pd.concat([df_tabela, df_medias], axis=1, ignore_index=False)
print(df)
#df.to_csv('./grafico_tabela.csv', encoding='utf-8')
