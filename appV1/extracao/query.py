from banco_de_dados.connections_db import ConnectionMysql, ConnectionPostg


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


def consulta_ocorrencias_progressao():
    cur = ConnectionPostg()
    sql = f"""
            SELECT t1.data_lan, t1.total_venda, t2.data_can, t2.total_can
            FROM
                (SELECT COUNT(codsercli)as total_venda, to_char(data_lan, 'YYYY-MM') data_lan
                FROM progressao
                GROUP BY 2 ORDER BY 2)AS t1 ,
            
                (SELECT COUNT(codsercli)as total_can, to_char(data_lan, 'YYYY-MM') data_lan, to_char(data_can, 'YYYY-MM') data_can
                FROM progressao
                WHERE data_can != '0001-01-01'
                GROUP BY 2, 3
                ORDER BY 2) as t2
            WHERE t1.data_lan = t2.data_lan
            ORDER BY 1, 3
        """
    cur.execute(sql)
    return cur.fetchall()


def verifica_plano_canceldo(codsercli):
    cur = ConnectionMysql()
    sql = f"""
            SELECT codcli, codsercli,nro_plano, data_lan, data_can, codcan
            FROM servicos_cli sc
            LEFT JOIN servicos s ON sc.codser = s.codser
            WHERE codcli = (SELECT codcli
            FROM servicos_cli sc
            LEFT JOIN servicos s ON sc.codser = s.codser
            WHERE codsercli = '{codsercli}'
            AND codcan = '01ALTERACA'
            and s.codgser != '01SERVER') 
            ORDER BY nro_plano Desc limit 1
        """
    cur.execute(sql)
    return cur.fetchall()


def validacao_real_de_cancelamento(codsercli):
    cur = ConnectionMysql()
    sql = f"""SELECT
            sc.codcli,
            sc.data_lan,
            sc.data_can,
            sc.codsercli
     
        FROM
            servicos_cli sc
  
            LEFT JOIN servicos s ON sc.codser = s.codser
            LEFT JOIN motivos_cancel mc ON sc.codcan = mc.codcan
        WHERE
            s.codgser != '01SERVER'
            and s.codgser != 'FEK00KZ3R2'
            and s.codgser != '01HOSPEDAG'
            and s.codgser != 'EUYM0O118I'
            and (mc.descri_can = 'COMPARTILHAMENTO ILEGAL'
            or mc.descri_can = 'CONDIÇÕES FINANCEIRA'
            or mc.descri_can = 'INADIMPLÊNCIA'
            or mc.descri_can = 'INSATISFAÇÃO'
            or mc.descri_can = 'INSATISFAÇÃO COM O ATENDIMENTO'
            or mc.descri_can = 'INSATISFAÇÃO COM O PREÇO'
            or mc.descri_can = 'INSATISFAÇÃO COM O SERVIÇO'
            or mc.descri_can = 'MUDANÇA DE ENDEREÇO'
            or mc.descri_can = 'MUDANÇA DE PROVEDOR'
            or mc.descri_can = 'OUTROS'
            or mc.descri_can = 'SUSPENSÃO POR TAREFA PROGRAMADA')
            AND sc.codsercli = '{codsercli}' """

    cur.execute(sql)
    return cur.fetchall()
