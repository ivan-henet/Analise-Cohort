from appV2.loads.envia_dados_db import DadosCohort
from appV2.tratamentoV2.agrupamento import agrupa_tabela_progressao
from appV2.tratamentoV2.cohort import cria_tabela_cohort
from appV2.tratamentoV2.progressao import cria_tabela_progressao

cria_tabela_progressao('2021-01-01', '2021-12-31')

agrupa_tabela_progressao()

cria_tabela_cohort()

inserir_dados = DadosCohort()
inserir_dados.limpa_tabela()
inserir_dados.ler_csv('Transformacao/tabela_cohort.csv')

