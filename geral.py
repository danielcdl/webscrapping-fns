import json
import requests
from datetime import date
from time import sleep

from tqdm import tqdm
import xlwt

colunas = ('A', 'B', 'C', 'D', 'E', 'F', 'G','H','I','J','K','L','M','N','O')
meses = ('Jan', 'Fev', 'Mar', 'Abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez', 'Valor Total')
nome_tabela = ('ATENCAO BÁSICA', 'VIGILÂNCIA EM SAÚDE', 'ASSISTÊNCIA FARMACÊUTICA')
cores = {'ATENCAO BÁSICA': 'green', 'VIGILÂNCIA EM SAÚDE': 'violet', 'ASSISTÊNCIA FARMACÊUTICA': 'light_blue'}
nome_tabela_covid = ('COMPETÊNCIA/ PARCELA', 'Nº OB', 'DATA OB', 'TIPO DE REPASSE',	'BANCO OB',	'AGÊNCIA OB',
    'CONTA OB', 'VALOR TOTAL', 'DESCONTO', 'LÍQUIDO', 'REJEIÇÃO', 'PROCESSO', 'Nº PROPOSTA', 'PORTARIA')

municipios = (
    {'nome': 'Anajás', 'cpfCnpjUg': 13715424000184, 'municipio': 150070},
    {'nome': 'Bagre', 'cpfCnpjUg': 13888332000104, 'municipio': 150110},
    {'nome': 'Breves', 'cpfCnpjUg': 17298800000133, 'municipio': 150180},
    {'nome': 'Curralinho', 'cpfCnpjUg': 11441240000148, 'municipio': 150280},
    {'nome': 'Gurupá', 'cpfCnpjUg': 12049775000130, 'municipio': 150310},
    {'nome': 'Melgaço', 'cpfCnpjUg': 11530230000189, 'municipio': 150450},
    {'nome': 'Portel', 'cpfCnpjUg': 11956268000118, 'municipio': 150580}
)

URL_ACAO = 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-acao'
URL_PAGAMENTO = 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-pagamento'

grupos = (12, 34, 35)

while True:
    tipo = input('Digite 1 para o ano atual ou 2 para anos anteriores\n')
    if tipo == '1':
        data = date.today()
        mes_atual = data.month
        ano = data.year
        break
    elif tipo == '2':
        mes_atual = 12
        try:
            ano = int(input('Digite o ano a ser pesquisado: '))
            if ano > 2008:
                break
            else:
                print('Digite uma data mais atual')
        except ValueError:
            print('Digite uma data válida')


dados_geral = {
    'ano': ano, 
    'blocos': 10,
    'count': 100,
    'estado': 'PA',
    'page': 1,
    'tipoConsulta': 2
}


def lista_chaves(parametros):
    chaves = {}
    descricoes = []
    while True:
        try:
            req = requests.get(URL_ACAO, params=parametros)
            if req.status_code == 200:
                i = 0
                resposta = json.loads(req.content)['resultado']['dados']
                for dado in resposta:
                    chave = dado['id']
                    if chave not in chaves:
                        chaves[chave] = i
                        descricoes.append(dado['descricao'])
                        i += 1
                break
            else:
                print('\nfalha', req.status_code)
        except requests.exceptions.ConnectionError:
            print('=' * 15)
            print('\nErro na conecção! tentando novamente...')
            print('=' * 15)
            sleep(1)
    return chaves, descricoes

def dados_tabela(parametros):
    tabela = {}
    while True:
        try:  
            req = requests.get(URL_ACAO, params=parametros)
            if req.status_code == 200:
                resposta = json.loads(req.content)['resultado']['dados']
                for dado in resposta:
                    chave = dado['id']
                    if chave != 0:
                        valor = dado['valorLiquido']
                        tabela[chave] = valor
                break
            else:
                print('=' * 15)
                print('\nfalha', req.status_code)
                print('=' * 15)
        except requests.exceptions.ConnectionError:
            print('=' * 15)
            print('\nErro na conecção! tentando novamente...')
            print('=' * 15)
            sleep(1)
    return tabela

def covid_tabela(parametros):
    tabela = []
    while True:
        try:  
            req = requests.get(URL_PAGAMENTO, params=parametros)
            if req.status_code == 200:
                resposta = json.loads(req.content)['resultado']['dados']
                for acao in resposta:
                    corona = (
                        acao['competencia'],
                        acao['numeroDocumentoSiafi'],
                        acao['dataCriacaoSiafi'],
                        acao['id']['esferaAdministrativa'],
                        acao['codigoBanco'],
                        acao['codigoAgencia'],
                        acao['contaCorrente'],
                        acao['valorTotal'],
                        acao['valorDescontoTotal'],
                        acao['valorLiquido'],
                        acao['motivoRejeicao'],
                        acao['id']['processoFormatado'],
                        '',
                        acao['nuPortaria']
                    )
                    tabela.append(corona)
                break
            else:
                print('=' * 15)
                print('falha', req.status_code)
                print('=' * 15)
        except requests.exceptions.ConnectionError:
            print('=' * 15)
            print('Erro na conecção! tentando novamente...')
            print('=' * 15)
            sleep(1)
    return tabela



planilha = xlwt.Workbook()
pbar = tqdm(total=len(municipios) * (len(grupos) +1) * mes_atual + 3, desc='Iniciando')
for municipio in municipios:
    pbar.desc = f"Baixando {municipio['nome']}"
    dados = dados_geral
    dados['cpfCnpjUg'] = municipio['cpfCnpjUg']
    dados['municipio'] = municipio['municipio']
    
    tabela_geral = []
    descricoes_geral = []
    for grupo in grupos:  
        dados['grupo'] = grupo
        chaves, descricoes = lista_chaves(dados)
        descricoes_geral.append(descricoes)
        tabela = []
        for i in range(len(chaves)):
            tabela.append([0]*12)
        for mes in range(1, mes_atual + 1):
            dados['mes'] = mes
            valores = dados_tabela(dados)
            for chave in valores:
                tabela[chaves[chave]][mes-1] = valores[chave]
            pbar.update(1)
        del dados['mes']
        tabela_geral.append(tabela)

    dados['grupo'] = 245
    dados['componentes'] = 175
    chaves = lista_chaves(dados)
    tabela = []
    del dados['grupo']
    for chave in chaves[0]:
        dados['acoes'] = chave
        valores = covid_tabela(dados)
        for valor in valores:
            tabela.append(valor)
        pbar.update(1)
    tabela_geral.append(tabela)
    del dados['acoes'] 
    del dados['componentes']

    #=============== Salvar Planilha ===========================
    bordas = xlwt.easyxf("borders: left thin, right thin, top thin, bottom thin;")
    bordas_negrito = xlwt.easyxf("font: bold on; borders: left thin, right thin, top thin, bottom thin;")
    bordas_left = xlwt.easyxf("borders: left thin;")

    aba = planilha.add_sheet(municipio['nome'])
    
    aba.col(1).width = 367 * 30
    for i in range(2, 14):
        aba.col(i).width = 367 * 13
    linha = 7
    indice = 0
    for nome in nome_tabela:
        bordas_top_bottom = xlwt.easyxf(f"font: bold on; borders: top thin, bottom thin; pattern: pattern solid, fore_colour {cores[nome]};")
        bordas_left_top_bottom = xlwt.easyxf(f"font: bold on; borders: left thin, top thin, bottom thin; pattern: pattern solid, fore_colour {cores[nome]};")
        bordas_fundo = xlwt.easyxf(f"font: bold on; borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_colour {cores[nome]};")
        aba.write(linha, 1, '', bordas_left_top_bottom)
        aba.write(linha, 14, '', bordas_left)
        aba.write(linha, 6, nome, bordas_top_bottom)
        linha += 1
        aba.write(linha, 1, '', bordas_fundo)
        for i in range(12):
            if i != 4:
                aba.write(linha - 1, i + 2, '', bordas_top_bottom)
            aba.write(linha, i + 2, meses[i], bordas_fundo)
        
        bordas.alignment.wrap = 1
        inicio_soma = linha + 2
        bordas.num_format_str = "#,##0.00"
        for linha_grupo, descricao in zip(tabela_geral[indice], descricoes_geral[indice]):    
            linha += 1
            aba.write(linha, 1, descricao, bordas)
            for k in range(12):
                aba.write(linha, k + 2, linha_grupo[k], bordas)
        linha += 1
        aba.write(linha, 1, 'Subtotal Componente', bordas_negrito)
        for k in range(12):
            aba.write(linha, k + 2, xlwt.Formula(f'SUM({colunas[k + 2]}{inicio_soma}:{colunas[k + 2]}{linha})'), bordas_negrito)
        linha += 2
        indice += 1

    bordas_top_bottom = xlwt.easyxf("font: bold on; borders: top thin, bottom thin; pattern: pattern solid, fore_colour yellow;")
    bordas_left_top_bottom = xlwt.easyxf("font: bold on; borders: left thin, top thin, bottom thin; pattern: pattern solid, fore_colour yellow;")
    bordas_fundo = xlwt.easyxf("font: bold on; borders: left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_colour yellow;")
    aba.write(linha, 1, '', bordas_left_top_bottom)
    aba.write(linha, 15, '', bordas_left)
    aba.write(linha, 6, 'RECURSOS DE CUSTEIO COVID-19', bordas_top_bottom)
    linha += 1
    for i in range(len(nome_tabela_covid)):
        if 0 < i != 5:
            aba.write(linha - 1, i + 1, '', bordas_top_bottom)
        aba.write(linha, i + 1, nome_tabela_covid[i], bordas_fundo)
    
    if len(tabela_geral) == 4:
        for linha_grupo in tabela_geral[3]:
            linha += 1
            for k in range(len(linha_grupo)):
                aba.write(linha, k + 1, linha_grupo[k], bordas)
    linha += 1
    aba.write(linha, 1, 'TOTAL   GERAL', bordas_negrito)
    for k in range(13):
        if k == 6 or k == 8:
            aba.write(linha, k + 2, xlwt.Formula(f'SUM({colunas[k + 2]}{inicio_soma}:{colunas[k + 2]}{linha})'), bordas_negrito)
        else:
            aba.write(linha, k + 2, '', bordas)
while True:
    try:
        planilha.save(f'Planilha de acompanhamento {ano}.xls')
        print('=' * 15)
        print('Arquivo salvo com SUCESSO!')
        print('=' * 15)
        break
    except PermissionError:
        print('=' * 15)
        print('Feche o arquivo para salva-lo com as alterações')
        print('=' * 15)
        sleep(5)
