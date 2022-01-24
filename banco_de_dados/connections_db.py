from banco_de_dados.engines import EnginePostgres, EngineMysql
import psycopg2 as ptg
import mysql.connector as db

class ConnectionPostg(EnginePostgres):
    def __init__(self):
        EnginePostgres.__init__(self)
        try:
            # cria a conexão com o dicionario db_config
            self.conn = ptg.connect(**self.config['postgres'])  # (**) para desempacotar o config
            self.cur = self.conn.cursor()
        except ptg.Error as e:
            print(f'Erro ao se conectar {e}')
            exit(1)  # parametro para sair da conexao

    # ---------------METODOS PARA MANIPULAÇÃO DE SQL ---------------#
    # metodo para entrar e retornar o objeto conexao
    def __enter__(self):
        return self

    # metodo para sair da conexão
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.conn.close()

    # metodo para retornar a conexão
    @property
    def connection(self):
        return self.conn

    # metodo para manipular o db
    @property
    def cursor(self):
        return self.cur

    # metodo para salvar as alterações no db
    def commit(self):
        self.connection.commit()
        return self.cur

    # metodo para retornar todos itens do bd
    def fetchall(self):
        return self.cursor.fetchall()

    # metodo para instrução SQL com ou sem parametros
    def execute(self, sql, params=None):
        self.cursor.execute(sql, params)

    # metodo para instrução SQL com ou sem parametros
    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()


class ConnectionMysql(EngineMysql):
    def __init__(self):
        EngineMysql.__init__(self)
        try:
            # cria a conexão com o dicionario db_config
            self.conn = db.connect(**self.config['mysql'])  # (**) para desempacotar o config
            self.cur = self.conn.cursor()
        except db.Error as e:
            print(f'Erro ao se conectar {e}')
            exit(1)  # parametro para sair da conexao

    # ---------------METODOS PARA MANIPULAÇÃO DE SQL ---------------#
    # metodo para entrar e retornar o objeto conexao
    def __enter__(self):
        return self

    # metodo para sair da conexão
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.conn.close()

    # metodo para retornar a conexão
    @property
    def connection(self):
        return self.conn

    # metodo para manipular o db
    @property
    def cursor(self):
        return self.cur

    # metodo para salvar as alterações no db
    def commit(self):
        self.connection.commit()
        return self.cur

    # metodo para retornar todos itens do bd
    def fetchall(self):
        response = self.cursor.fetchall()
        self.conn.close()
        return response

    # metodo para instrução SQL com ou sem parametros
    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    # metodo para instrução SQL com ou sem parametros
    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def fetchone(self):
        response = self.cursor.fetchone()
        self.conn.close()
        return response
