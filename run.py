from carregamento.envia_dados_db import DadosProgressao
from carregamento.tabela_cohort import DadosCohort
from carregamento.grafico import GraficoTabela

# Defina a data de inicio e fim para analise
# data_inicio = '2021-01-01'
# data_fim = '2021-12-31'
# #prog = Progressao(data_inicio, data_fim)
#
#
# progressao = DadosProgressao()
# progressao.limpa_tabela()
# progressao.ler_csv('../progressao.csv')
#
#
# cohort = DadosCohort()
# cohort.ler_csv('../cohort.csv')

a = GraficoTabela()
a.ler_csv('./tratamento/grafico_tabela.csv')
