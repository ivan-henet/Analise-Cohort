import csv

from banco_de_dados.connections_db import ConnectionPostg


class GraficoTabela(ConnectionPostg):
    """Conecta com o Banco de dados PostegreSql"""

    def __init__(self):
        ConnectionPostg.__init__(self)

    def limpa_tabela(self):
        try:
            sql = """ TRUNCATE TABLE tabela_cohort; """
            self.execute(sql)
        except ConnectionError as e:
            return e

    def inserir_dados_no_bd(self, *args):
        """insere dados dos planos suspensos respectivo ao codsercli no postgresql"""
        try:
            sql = """INSERT INTO tabela_cohort(janeiro,fevereiro,marco,abril,maio,junho,julho,agosto,setembro,outubro,
            novembro,dezembro,medias)
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
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
                self.inserir_dados_no_bd(
                    row['janeiro'],
                    row['fevereiro'],
                    row['marco'],
                    row['abril'],
                    row['maio'],
                    row['junho'],
                    row['julho'],
                    row['agosto'],
                    row['setembro'],
                    row['outubro'],
                    row['novembro'],
                    row['dezembro'],
                    row['medias'],
                    #row['crescimento'],

                )

            print('Success')
        except ConnectionError as e:
            print(f'Erro ao inserir os dados: Func: insert_csv: Error: {e}')
            return e
