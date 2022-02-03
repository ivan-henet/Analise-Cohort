from appV1.carregamento.insert_cohort import DadosCohort

from appV1.tratamento import cria_tabela_cohort


dt_inicio = '2021-01-01'
dt_fim = '2021-12-01'

# cria_tabela_progressao(dt_inicio, dt_fim)
# progressao = DadosProgressao()
# progressao.limpa_tabela()
# progressao.ler_csv('./tratamento/tabela_progressao.csv')


cria_tabela_cohort()
cohort = DadosCohort()
cohort.limpa_tabela()
cohort.ler_csv('./tabela_cohort.csv')
