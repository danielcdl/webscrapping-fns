import pandas as pd
import requests
from bs4 import BeautifulSoup

#=========== Pesquisas ===========
detalhada = {
    'custeio': {
        'assistencia_farmaceutica': {
            'total': 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-acao?ano=2020&blocos=10&count=10&cpfCnpjUg=11956268000118&estado=PA&grupo=35&municipio=150580&page=1&tipoConsulta=2',
            'detalhe':'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-pagamento?acoes=62420&ano=2020&blocos=10&count=25&cpfCnpjUg=11956268000118&estado=PA&municipio=150580&page=1&tipoConsulta=2'
        },
        'atencao_basica': {
            'geral':'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-acao?ano=2020&blocos=10&count=10&cpfCnpjUg=11956268000118&estado=PA&grupo=12&municipio=150580&page=1&tipoConsulta=2',
            0: {'nome': 'AGENTE COMUNITÁRIO DE SAÚDE', 'url': 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-pagamento?acoes=62060&ano=2020&blocos=10&count=25&cpfCnpjUg=11956268000118&estado=PA&municipio=150580&page=1&tipoConsulta=2'},
            1: {'nome': 'APOIO À MANUTENÇÃO DOS POLOS DE ACADEMIA DA SAÚDE', 'url': 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-pagamento?acoes=62458&ano=2020&blocos=10&count=25&cpfCnpjUg=11956268000118&estado=PA&municipio=150580&page=1&tipoConsulta=2'},
            2: {'nome': 'INCENTIVO FINANCEIRO DA APS - FATOR COMPENSATÓRIO DE TRANSIÇÃO', 'url': 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-pagamento?acoes=65586&ano=2020&blocos=10&count=25&cpfCnpjUg=11956268000118&estado=PA&municipio=150580&page=1&tipoConsulta=2'},
            3: {'nome': 'INCENTIVO FINANCEIRO DA APS - DESEMPENHO', 'url': 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-pagamento?acoes=65580&ano=2020&blocos=10&count=25&cpfCnpjUg=11956268000118&estado=PA&municipio=150580&page=1&tipoConsulta=2'},
            4: {'nome': 'INCENTIVO PARA AÇÕES ESTRATÉGICAS', 'url': 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-pagamento?acoes=65582&ano=2020&blocos=10&count=25&cpfCnpjUg=11956268000118&estado=PA&municipio=150580&page=1&tipoConsulta=2'},
            5: {'nome': 'IMPLEMENTAÇÃO DE POLÍTICAS PARA A REDE CEGONHA', 'url': 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-pagamento?acoes=65178&ano=2020&blocos=10&count=25&cpfCnpjUg=11956268000118&estado=PA&municipio=150580&page=1&tipoConsulta=2'}
        },
        'media_e_alta_complexidade': {
            'geral': 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-acao?ano=2020&blocos=10&count=10&cpfCnpjUg=11956268000118&estado=PA&grupo=14&municipio=150580&page=1&tipoConsulta=2',
            0: {'acao_detalhada': 'SAMU 192', 'url': 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-pagamento?acoes=62079&ano=2020&blocos=10&count=25&cpfCnpjUg=11956268000118&estado=PA&municipio=150580&page=1&tipoConsulta=2'},
            1: {'acao_detalhada': 'ATENÇÃO À SAÚDE DA POPULAÇÃO PARA PROCEDIMENTOS NO MAC', 'url': 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-pagamento?acoes=61659&ano=2020&blocos=10&count=25&cpfCnpjUg=11956268000118&estado=PA&municipio=150580&page=1&tipoConsulta=2'}
        },
        'atencao_especializada': {
            'geral': 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-acao?ano=2020&blocos=10&count=10&cpfCnpjUg=11956268000118&estado=PA&grupo=121&municipio=150580&page=1&tipoConsulta=2'
        },
        'corona_virus': {
            'geral': 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-acao?ano=2020&blocos=10&componentes=175&count=10&cpfCnpjUg=11956268000118&estado=PA&grupo=245&municipio=150580&page=1&tipoConsulta=2'
        },
        'gestao_do_sus': {
            'geral': 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-acao?ano=2020&blocos=10&count=10&cpfCnpjUg=11956268000118&estado=PA&grupo=17&municipio=150580&page=1&tipoConsulta=2',
            0: {'acao_detalhada': 'IMPLEMENTAÇÃO DA SEGURANÇA ALIMENTAR E NUTRICIONAL NA SAÚDE', 'url': 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-pagamento?acoes=63402&ano=2020&blocos=10&count=25&cpfCnpjUg=11956268000118&estado=PA&municipio=150580&page=1&tipoConsulta=2'}
        },
        'vigilancia_em_saude': {
            'geral': 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-acao?ano=2020&blocos=10&count=10&cpfCnpjUg=11956268000118&estado=PA&grupo=34&municipio=150580&page=1&tipoConsulta=2',
            0: {'acao_detalhada': 'INCENTIVO FINANCEIRO AOS ESTADOS, DISTRITO FEDERAL E MUNICÍPIOS PARA A VIGILÂNCIA EM SAÚDE - DESPESAS DIVERSAS', 'url': 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-pagamento?acoes=62109&ano=2020&blocos=10&count=25&cpfCnpjUg=11956268000118&estado=PA&municipio=150580&page=1&tipoConsulta=2'},
            1: {'acao_detalhada': 'INCENTIVO FINANCEIRO AOS ESTADOS, DISTRITO FEDERAL E MUNICÍPIOS PARA EXECUÇÃO DE AÇÕES DE VIGILÂNCIA SANITÁRIA', 'url': 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-pagamento?acoes=62113&ano=2020&blocos=10&count=25&cpfCnpjUg=11956268000118&estado=PA&municipio=150580&page=1&tipoConsulta=2'},
            2: {'acao_detalhada': 'ASSISTÊNCIA FINANCEIRA COMPLEMENTAR AOS ESTADOS, DISTRITO FEDERAL E MUNICÍPIOS PARA AGENTES DE COMBATE ÀS ENDEMIAS', 'url': 'https://consultafns.saude.gov.br/recursos/consulta-detalhada/detalhe-pagamento?acoes=62110&ano=2020&blocos=10&count=25&cpfCnpjUg=11956268000118&estado=PA&municipio=150580&page=1&tipoConsulta=2'}
        }
    },
    'investimento': {}
}

print(detalhada)

req = requests.get(detalhada['custeio']['assistencia_farmaceutica']['total'])
if req.status_code == 200:
    print('Requisição bem sucedida!')
    content = req.content

    soup = BeautifulSoup(content, 'html.parser')
    print(soup)

else:
    print('falha', req.status_code)