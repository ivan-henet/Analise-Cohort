from carregamento.insert_cohort import DadosCohort

from carregamento.insert_progressao import DadosProgressao

from tratamento.progressao import cria_tabela_progressao
from tratamento.tabela_cohort import cria_tabela_cohort


dt_inicio = '2021-01-01'
dt_fim = '2021-12-01'


#cria_tabela_progressao(dt_inicio, dt_fim)
progressao = DadosProgressao()
progressao.limpa_tabela()
progressao.ler_csv('./tratamento/tabela_progressao.csv')


cria_tabela_cohort()
cohort = DadosCohort()
cohort.limpa_tabela()
cohort.ler_csv('./tratamento/tabela_cohort.csv')
