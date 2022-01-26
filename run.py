from carregamento.insert_cohort import DadosCohort
from carregamento.insert_ocorrencias import DadosOcorrencias
from carregamento.insert_progressao import DadosProgressao
#
# progressao = DadosProgressao()
# progressao.limpa_tabela()
# progressao.ler_csv('./tratamento/tabela_progressao.csv')



cohort = DadosCohort()
cohort.limpa_tabela()
cohort.ler_csv('./tratamento/tabela_cohort.csv')
