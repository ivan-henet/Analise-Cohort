from banco_de_dados.connections_db import ConnectionMysql, ConnectionPostg


def consulta_planos_cancelados(codcli, data_can):
    cur = ConnectionMysql()
    sql = f"""
            SELECT 
            sc.codcli, 
            sc.codsercli,
            sc.data_lan, 
            sc.data_can,
            codcan,
            nro_plano
            FROM servicos_cli sc  
            LEFT JOIN servicos s ON sc.codser = s.codser
            where sc.codcli = '{codcli}' 
            and sc.data_lan = '{data_can}'
            and s.codgser != '01SERVER'
            """

    cur.execute(sql)
    return cur.fetchall()


def consulta_planos_lancados_por_periodo(data_inicio, data_fim):
    cur = ConnectionMysql()
    sql = f"""
            SELECT 
            sc.codcli, 
            sc.codsercli,
            sc.data_lan, 
            sc.data_can,
            codcan,
            nro_plano
            FROM servicos_cli sc  
            LEFT JOIN servicos s ON sc.codser = s.codser
            where s.codgser != '01SERVER' 
            and sc.data_lan between '{data_inicio}' and '{data_fim}'
            and sc.data_hab is True
            and sc.codcli != '8116';
        """
    cur.execute(sql)
    return cur.fetchall()



def consulta_dados():
    cur = ConnectionPostg()
    sql = f"""SELECT
            t1.lancamento,
            t1.total_venda,
            t2.cancelado,
            t2.total_cancelado,
            (t1.total_venda - t2.total_cancelado) AS saldo
            FROM
            (SELECT count(id) total_venda, 
            to_char(data_lan, 'YYYY-MM') lancamento
            FROM progressao_cancelamento
            GROUP BY 2
            ORDER BY 2) AS t1,
            (SELECT count(id) total_cancelado, 
            to_char(data_lan, 'YYYY-MM') lancamento,
             to_char(data_can, 'YYYY-MM') cancelado
            FROM progressao_cancelamento
            WHERE data_can != '0001-01-01'
            --AND to_char(data_can, 'YYYY-MM') != '2021-01' 
            GROUP BY 2,3
            ORDER BY 2) AS t2
            WHERE t1.lancamento = t2.lancamento
            ORDER BY 1,3 """

    cur.execute(sql)
    return cur.fetchall()

