import pandas as pd

from extracao.querys import consulta_vendidos_e_cancelados, faz_progressao_de_planos


def cria_tabela_progressao(inicio, fim):
    result_cancelados = consulta_vendidos_e_cancelados(inicio, fim)

    result_cancelados = [[i[0], i[1], i[2], i[3], i[4], i[5], i[6]] for i in result_cancelados]

    planos_cancelados = []
    erros = []

    def verifica_se_e_alteracao(data_can, codcan):
        if codcan == '01ALTERACA':
            return 'alteracao'

        elif data_can is None:
            return 'ativo'

        elif data_can is not None and codcan != '01ALTERACA':
            return 'cancelado'

    for planos in result_cancelados:
        CODSERCLI = planos[1]
        DATA_CAN = planos[4]

        if DATA_CAN != '0000-00-00':
            planos_cancelados.append(planos)

    array_planos = []

    for cod in planos_cancelados:

        codcli = cod[0]
        codsercli = cod[1]
        data_lan = cod[2]
        data_can = cod[4]
        codcan = cod[5]

        condicao = verifica_se_e_alteracao(data_can, codcan)

        if condicao == 'cancelado':
            array_planos.append([codsercli, data_can])

        elif condicao == 'alteracao':

            nro_plano = cod[6]
            data_next = data_can

            status = True
            cods = []

            while status:
                progressao = faz_progressao_de_planos(codcli, data_next)

                if len(progressao) > 0:

                    for prog in progressao:
                        print(prog)
                        condicao = verifica_se_e_alteracao(prog[3], prog[4])

                        if prog[1] not in cods:
                            cods.append(prog[1])

                            if prog[5] > nro_plano:

                                if condicao == 'cancelado':
                                    array_planos.append([codsercli, prog[3]])
                                    status = False

                                elif condicao == 'ativo':
                                    array_planos.append([codsercli, '0001-01-01'])
                                    status = False

                                else:
                                    data_next = prog[3]
                                    nro_plano = prog[5]

                        else:
                            erros.append(prog[1])
                            status = False

                else:
                    status = False
        print(codsercli)
    for pos in array_planos:
        for dados in result_cancelados:
            if pos[0] == dados[1]:
                dados[4] = pos[1]
            if len(dados[5]) <= 0:
                dados[5] = 'ATIVO'
            if dados[4] == '0000-00-00':
                dados[4] = '0001-01-01'

    colunas = ['codcli', 'codsercli', 'data_lan', 'data_hab', 'data_can', 'codcan','nro_plano']
    df = pd.DataFrame(result_cancelados, columns=colunas)
    df_erros = pd.DataFrame(erros, columns=['erros'])
    erros_csv = df_erros.to_csv('erros.csv', index=False)
    arquivo_csv = df.to_csv('./tabela_progressao.csv', sep=',', encoding='utf-8', index=False)





