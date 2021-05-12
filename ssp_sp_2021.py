#!/usr/bin/python3

# bibliotecas usadas
import codecs
import time
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import Select

# Driver para simular o acesso via Firefox
# baixar geckodriver em https://github.com/mozilla/geckodriver/releases
# seguir instruções em
#    https://medium.com/beelabacademy/baixando-e-configurando-o-geckodriver-no-ubuntu-dc2fe14d91c

# Principal referência de apoio à raspagem de dados:
#  https://blog.4linux.com.br/web-scraping-python-selenium-e-beautifulsoup/

# Abre arquivo de texto que guardará o resultado da raspagem de dados
f = codecs.open("./ssp", "w", "utf-8")
f.write('cidade|mes|natureza|n\n')

# municípios
cidades = [
    'Americana'
    ,'Matão'
    ,'Monte Alto'
    ,'Taquaritinga'
    ,'Valinhos'
    ,'Vinhedo'
]

# abre a janela do Firefox
browser = webdriver.Firefox()
url = "http://www.ssp.sp.gov.br/Estatistica/Pesquisa.aspx"

for cidade in cidades:
    # acessa o url no navegador aberto pelo script
    browser.get(url)

    # aguarda 5 seguros
    # time.sleep(5)

    # municipio
    municipio  = Select( browser.find_element_by_xpath('//*[@id="conteudo_ddlMunicipios"]') )
    municipio.select_by_visible_text( cidade )
    # time.sleep(2)  # aguarda alguns segundos

    # acha e clica no botão 'Procurar'
    browser.find_element_by_xpath('//*[@id="conteudo_btnMensal"]').click()

    # aguarda 10 seguros até a página carregar por completo
    # time.sleep(5)

    # guarda o resultado da busca no objeto 'res'
    res  = browser.find_element_by_xpath(".//html")

    # seleciona a estrutura em html do resultado da busca
    html = res.get_attribute('innerHTML')

    # organiza o acesso aos tags html através do BeautifulSoup
    soup = BeautifulSoup( html, 'html.parser')

    # 0 --> 2021
    # 1 --> 2020
    # 2 --> 2019
    for k in [0,1,2]:
        table = soup.findAll('table')[k]

        ano = 2021 - k
        ano = str(ano)

        # acesso ao conteúdo de cada linha, iniciando na linha 2
        for row in table.findAll('tr')[1:]:

            natureza = row.findAll('td')[0].text.strip()
            count_mes = 1
            for col in row.findAll('td')[1:-1]:

                n = col.text.strip()
                if n == '...':
                    n = '0'

                # grava resultado no arquivo de conexão 'f'
                f.write(
                    cidade + '|' +
                    natureza + '|' +
                    '' + '|' +
                    ano + '-' + str(count_mes).zfill(2) + '-01|' +
                    n +
                    '\n'
                )
                count_mes = count_mes + 1
                
# fecha navegador
browser.close()

# fecha conexão com arquivo
f.close()

