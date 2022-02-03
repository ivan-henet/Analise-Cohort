from banco_de_dados.connections_db import ConnectionMysql


def consulta_vendidos_e_cancelados(dt_inicio, dt_fim):
    cur = ConnectionMysql()
    sql = f"""
        SELECT
        sc.codcli,
        sc.codsercli,
        sc.data_lan,
        sc.data_hab,
        IFNULL(sc.data_can,'0001-01-01') as data_can,
        sc.codcan, 
        sc.nro_plano
        FROM servicos_cli sc
        LEFT JOIN servicos s ON s.codser = sc.codser
        LEFT JOIN servicos_cli sc_p ON sc_p.codsercli=sc.codsercli_p AND sc.codsercli_p <>''
        WHERE sc_p.codsercli IS NULL
        and sc.data_hab != '0000-00-00'
        and sc. data_lan between '{dt_inicio}' and '{dt_fim}'
        and s.codgser NOT IN ('01SERVER','01HOSPEDAG', 'EUYM0O118I')
        GROUP BY sc.codsercli """

    cur.execute(sql)
    return cur.fetchall()


def faz_progressao_de_planos(codcli, data_can):
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

