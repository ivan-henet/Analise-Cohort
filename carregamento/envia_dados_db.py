import csv

from banco_de_dados.connections_db import ConnectionPostg


class DadosProgressao(ConnectionPostg):
    """Conecta com o Banco de dados PostegreSql"""

    def __init__(self):
        ConnectionPostg.__init__(self)

    def limpa_tabela(self):
        try:
            sql = """ TRUNCATE TABLE progressao_cancelamento; """
            self.execute(sql)
        except ConnectionError as e:
            return e

    def inserir_dados_no_bd(self, *args):
        """insere dados dos planos suspensos respectivo ao codsercli no postgresql"""
        try:
            sql = """INSERT INTO progressao_cancelamento(codcli,codsercli,data_lan,data_can,nro_plano)
             VALUES (%s,%s,%s,%s,%s) """
            self.execute(sql, args)
            self.commit()
        except ConnectionError as e:
            print(f'Erro ao inserir os dados: Func: inset_data_ptg: Error: {e}')
            return e

    def ler_csv(self, filename):
        """Ler o arquivo e insere as linhas no banco de dados."""
        try:
            plan_csv = csv.DictReader(open(filename, encoding='utf-8'))
            for row in plan_csv:
                print(row['codcli'])
                self.inserir_dados_no_bd(
                    row['codcli'],
                    row['codsercli'],
                    row['data_lan'],
                    row['data_can'],
                    row['nro_plano'],
                )

            print('Success')
        except ConnectionError as e:
            print(f'Erro ao inserir os dados: Func: insert_csv: Error: {e}')
            return e
