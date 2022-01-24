import datetime
import pandas as pd

from extracao.query import consulta_planos_cancelados, consulta_planos_lancados_por_periodo


class Progressao:
    """
    Faz a progressao de cancelamento dos planos a partir do periodo informado(data_inicio, data_fim)
    :arg: data_ini = '2021-01-01'
    :arg: data_fim = '2021-01-30'
    """

    def __init__(self, data_inicio, data_fim):
        self.data_fim = data_fim
        self.data_inicio = data_inicio
        self.arquivo = []

    def verifica_se_e_alteracao(self, data_can, codcan):
        if codcan == '01ALTERACA':
            return 'alteracao'

        elif data_can is None:
            return 'ativo'

        elif data_can is not None and codcan != '01ALTERACA':
            return 'cancelado'

    def cria_dicionario(self, codcli, codsercli, data_lan, data_can, nro_plano):
        self.arquivo.append(
            dict(codcli=codcli, codsercli=codsercli, data_lan=data_lan, data_can=data_can,
                 nro_plano=nro_plano))
        return self.arquivo

    def faz_progressao_dos_planos(self):

        result_consulta = consulta_planos_lancados_por_periodo(self.data_inicio, self.data_fim)
        result_codsercli = sorted(result_consulta, key=lambda x: x[5])

        for planos in result_codsercli:
            CODCLI = planos[0]
            CODSERCLI = planos[1]
            DATA_LAN = planos[2]
            DATA_CAN = planos[3]
            codcan = planos[4]

            condicao = self.verifica_se_e_alteracao(DATA_CAN, codcan)

            if condicao == 'ativo':
                self.cria_dicionario(codcli=CODCLI, codsercli=CODSERCLI, data_lan=DATA_LAN, data_can=datetime.date(
                    1, 1, 1), nro_plano=planos[5])

            elif condicao == 'cancelado':
                self.cria_dicionario(codcli=CODCLI, codsercli=CODSERCLI, data_lan=DATA_LAN, data_can=DATA_CAN,
                                     nro_plano=planos[5])

            elif condicao == 'alteracao':

                data_next = DATA_CAN

                progressao = consulta_planos_cancelados(CODCLI, data_next)

                for prog in progressao:
                    condicao = self.verifica_se_e_alteracao(prog[3], prog[4])

                    if condicao == 'ativo':
                        self.cria_dicionario(codcli=CODCLI, codsercli=CODSERCLI, data_lan=DATA_LAN,
                                             data_can=datetime.date(1, 1, 1), nro_plano=prog[5])

                    elif condicao == 'cancelado':
                        self.cria_dicionario(codcli=CODCLI, codsercli=CODSERCLI, data_lan=DATA_LAN, data_can=prog[3],
                                             nro_plano=prog[5])

                    else:
                        data_next = prog[3]

            print(CODCLI, DATA_CAN)
        return self.arquivo

    def gera_arquivo_csv(self):
        arquivo_csv = pd.DataFrame(self.arquivo)
        arquivo_csv.to_csv('./progressao.csv', sep=',', encoding='utf-8')


if __name__ == '__main__':
    ...
    inicio = '2021-01-01'
    fim = '2021-12-31'
    criar = Progressao(inicio, fim)
    criar.faz_progressao_dos_planos()
    criar.gera_arquivo_csv()
    # 1335
