#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import time
from selenium import webdriver
from bs4 import BeautifulSoup

# Abre arquivo de texto que guardará o resultado da raspagem de dados
f = codecs.open("../ssp_sp", "w", "utf-8")
f.write('municipio|delito|mes|valor\n')

# abre a janela do Firefox
browser = webdriver.Firefox()
url = "http://www.ssp.sp.gov.br/novaestatistica/Pesquisa.aspx"

# Lista de Municípios para os quais a estatística será baixada
Municipios = [ 'Aguaí'
              ,'Águas de Lindóia'
              ,'Amparo'
              ,'Artur Nogueira'
              ,'Caconde'
              ,'Casa Branca'
              ,'Cosmopólis'
              ,'Espírito Santo do Pinhal'
              ,'Estiva Gerbi'
              ,'Holambra'
              ,'Itapira'
              ,'Itobi'
              ,'Jaguariúna'
              ,'Lindóia'
              ,'Mocóca'
              ,'Mogi Mirim'
              ,'Mogi Guaçu'
              ,'Pedreira'
              ,'Santo Antônio de Posse'
              ,'Santo Antonio do Jardim'
              ,'São João da Boa Vista'
              ,'São José do Rio Pardo'
              ,'São Sebastião da Grama'
              ,'Serra Negra'
              ,'Socorro'
              ,'Vargem Grande do Sul'
             ]


for Municipio in Municipios:

    print 'Baixando ' + Municipio + '.'*3,

    browser.get(url)    # acessa o url no navegador aberto pelo script

    # encontra o combo box dos municípios de SP, seleciona a cidade e atualiza a página para acessar os detalhes
    browser.find_element_by_name('ctl00$ContentPlaceHolder1$ddlMunicipios')
    browser.find_element_by_name('ctl00$ContentPlaceHolder1$ddlMunicipios').send_keys(Municipio.decode('utf-8'))
    browser.find_element_by_name('ctl00$ContentPlaceHolder1$ddlMunicipios').submit()

    # acha o botão Ocorrencias 'Policiais registradas por Mes'
    browser.find_element_by_id('ContentPlaceHolder1_btnMensal').click()

    time.sleep(5)

    for indice in ['0','1','2']:

        ano     = browser.find_element_by_id('ContentPlaceHolder1_repAnos_lbAno_'+indice).text
        tabela  = browser.find_element_by_id('ContentPlaceHolder1_repAnos_gridDados_'+indice).get_attribute('innerHTML')
        tblsoup = BeautifulSoup(tabela)

        Mes = {'Jan' : '-01-01',
               'Fev' : '-02-01',
               'Mar' : '-03-01',
               'Abr' : '-04-01',
               'Mai' : '-05-01',
               'Jun' : '-06-01',
               'Jul' : '-07-01',
               'Ago' : '-08-01',
               'Set' : '-09-01',
               'Out' : '-10-01',
               'Nov' : '-11-01',
               'Dez' : '-12-01'
        }

        for linha in range(1,20):
                for coluna in range(1,13):

                        descricao = tblsoup.findAll("tr")[linha].findAll("td")[0].string.title()
                        mes_abrev = tblsoup.findAll("th")[coluna].string
                        mes       = Mes[mes_abrev]
                        valor     = tblsoup.findAll("tr")[linha].findAll("td")[coluna].string
                        valor     = valor.replace("...","0")

                        f.write(
                                 Municipio.decode('utf-8')
                                 + '|'
                                 + descricao
                                 + '|'
                                 + ano + mes
                                 + '|'
                                 + valor
                                 + '\n'
                                )
    print 'ok!'

browser.close()

f.close()
