class EnginePostgres:
    """Engine de Produção"""

    def __init__(self):
        self.config = {
            'postgres': {
                'host': 'ec2.henet.com.br',
                #'host': 'postgres',
                'database': 'analise_clientes',
                'user': 'ivandev',
                'password': 'ivan@ads04',
                'port': 5432
            }
        }


class EngineMysql:
    """Conexao"""
    def __init__(self):
        self.config = {
            'mysql': {
                'database': 'henet',
                'user': 'henet',
                'password': '0Y3Prx1f59',
                'host': '177.38.245.178',
                'port': 3306,
            }
        }


# class EnginePostgres:
#     """Engine de desenvolvimento"""
#
#     # def __init__(self):
#     #     self.config = {
#     #         'postgres': {
#     #             'host': 'localhost',
#     #             #'host': 'postgres',
#     #             'database': 'desenvolvimento',
#     #             'user': 'postgres',
#     #             'password': 'henet',
#     #             'port': 5432
#     #         }
#     #     }
