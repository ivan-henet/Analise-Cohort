import csv

from banco_de_dados.connections_db import ConnectionPostg


class DadosCohort(ConnectionPostg):
    """Conecta com o Banco de dados PostegreSql"""

    def __init__(self):
        ConnectionPostg.__init__(self)

    def limpa_tabela(self):
        try:
            sql = """ TRUNCATE TABLE cohort; """
            self.execute(sql)
        except ConnectionError as e:
            return e

    def inserir_dados_no_bd(self, *args):
        """insere dados dos planos suspensos respectivo ao codsercli no postgresql"""
        try:
            # sql = """INSERT INTO cohort(jan,fev,mar,abr,mai,jun,jul,ago,sete,outu,nov,dez,medias,churn)
            #  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
            sql = """INSERT INTO cohort(index,janeiro,feveveiro,marco,abril,maio,junho,julho,agosto,setembro,outubro,novembro,dezembro,medias,churn)
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
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
                    row['index'],
                    row['jan'],
                    row['fev'],
                    row['mar'],
                    row['abr'],
                    row['mai'],
                    row['jun'],
                    row['jul'],
                    row['ago'],
                    row['set'],
                    row['out'],
                    row['nov'],
                    row['dez'],
                    row['medias'],
                    row['churn'],
                )

            print('Success')
        except ConnectionError as e:
            print(f'Erro ao inserir os dados: Func: insert_csv: Error: {e}')
            return e


if __name__ == '__main__':
    ...