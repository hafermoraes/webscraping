#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Importa as bibliotecas
#import pdb                     # debugger
import codecs                  # utf-8
import re                      # expressoes regulares
import urllib2                 # navegacao na internet
from bs4 import BeautifulSoup  # parsing

#pdb.set_trace()

# vetor com cidades das quais as informações serão levantadas
selecao_cidades = [ 'aguai'
                   ,'Águas-de-lindoia'
                   ,'amparo'
                   ,'artur-nogueira'
                   ,'caconde'
                   ,'casa-branca'
                   ,'cosmopolis'
                   ,'espirito-santo-do-pinhal'
                   ,'estiva-gerbi'
                   ,'holambra'
                   ,'itapira'
                   ,'itobi'
                   ,'jaguariuna'
                   ,'lindoia'
                   ,'mococa'
                   ,'mogi-mirim'
                   ,'mogi-guacu'
                   ,'pedreira'
                   ,'santo-antonio-de-posse'
                   ,'santo-antonio-do-jardim'
                   ,'sao-joao-da-boa-vista'
                   ,'sao-jose-do-rio-pardo'
                   ,'sao-sebastiao-da-grama'
                   ,'serra-negra'
                   ,'socorro'
                   ,'vargem-grande-do-sul'
                  ]

# Abre arquivo de texto que guardará o resultado da raspagem de dados
f = codecs.open("../ibge_cidades", "w", "utf-8")
f.write('municipio|descr1|descr2|valor|texto\n')

# Abre página do IBGE do estado de SP
html_SP = urllib2.urlopen('http://cidades.ibge.gov.br/xtras/uf.php?lang=&coduf=35&search=sao-paulo').read()

# Converte o conteúdo da pagina em HTML para o BeautifulSoup poder ler os tags
soup_SP = BeautifulSoup(html_SP)

# Visita cada link da pagina que contenha 'codmun'
for link in soup_SP.find_all('a'):

        pagina_Municipio = link.get('href').encode("utf-8")

        if "codmun" in pagina_Municipio:

            cidade = link.get('href').encode("utf-8").split('search=sao-paulo|')[1]

            if cidade in selecao_cidades:

                # ----- acesso ao link do Município e tratamento de dados
                url_base       = "http://cidades.ibge.gov.br/xtras/"
                url_Municipio  = url_base + pagina_Municipio
                html_Municipio = urllib2.urlopen(url_Municipio).read()
                soup_Municipio = BeautifulSoup(html_Municipio)
                # -------------------------------------------------------

                # ----- Detalhes do Município ---------------------------
                nome_cidade = soup_Municipio.find('span',{'class':'municipio titulo'}).text
                f.write(
                        nome_cidade +
                        '|info_basicas|habitantes_2014|' +
                        soup_Municipio.find_all('td',{'class':'valor'})[0].get_text().replace('.','') +
                        '|\n'
                       )
                f.write(
                        nome_cidade +
                        '|info_basicas|habitantes_2010|' +
                        soup_Municipio.find_all('td',{'class':'valor'})[1].get_text().replace('.','') +
                        '|\n'
                       )
                f.write(
                        nome_cidade +
                        '|info_basicas|area_km2|' +
                        soup_Municipio.find_all('td',{'class':'valor'})[2].get_text().replace(',','') +
                        '|\n'
                       )
                f.write(
                        nome_cidade +
                        '|info_basicas|hab_por_km2|' +
                        soup_Municipio.find_all('td',{'class':'valor'})[3].get_text().replace(',','') +
                        '|\n'
                       )
                f.write(
                        nome_cidade +
                        '|info_basicas|codigo_municipio|' +
                        soup_Municipio.find_all('td',{'class':'valor'})[4].get_text() +
                        '|\n'
                       )
                f.write(
                        nome_cidade +
                        '|info_basicas|gentilico||' +
                        soup_Municipio.find_all('td',{'class':'valor'})[5].get_text() +
                        '\n'
                       )
                f.write(
                        nome_cidade +
                        '|info_basicas|prefeito||' +
                        soup_Municipio.find_all('td',{'class':'valor'})[6].get_text().title() +
                        '\n'
                       )
                # -------------------------------------------------------

                # ----- Frota -------------------------------------------
                busca  = 'frota-2014'
                url    = soup_Municipio.find('a', href=re.compile(busca)).get('href').encode('utf-8')
                url    = url_base + url
                html   = urllib2.urlopen(url).read()
                soup   = BeautifulSoup(html)

                tabela = soup.find('table',{'class':'dados'})
                for linha in tabela.findAll('tr'):
                    f.write(
                            nome_cidade +
                            '|frota|' +
                            linha.findAll('td')[0].get_text().strip() +  # 1a coluna --> tipo de veículo
                            '|' +
                            linha.findAll('td')[1].get_text().replace('.','') + # 2a coluna --> qtde
                            '|\n'
                           )
                # -------------------------------------------------------


                # ----- Representação Política --------------------------
                busca  = 'representacao-politica-2014'
                url    = soup_Municipio.find('a', href=re.compile(busca)).get('href').encode('utf-8')
                url    = url_base + url
                html   = urllib2.urlopen(url).read()
                soup   = BeautifulSoup(html)

                tabela = soup.find('table',{'class':'dados'})
                for linha in tabela.findAll('tr'):
                    f.write(
                            nome_cidade +
                            '|representacao_politica|' +
                            linha.findAll('td')[0].get_text() +  #  descritivo
                            '|' +
                            linha.findAll('td')[1].get_text().replace('.','').replace(',','.') + # qtde/percentual votos
                            '|\n'
                           )
                # -------------------------------------------------------

                # ----- Instituições Financeiras ------------------------
                busca  = 'instituicoes-financeiras-2014'
                url    = soup_Municipio.find('a', href=re.compile(busca)).get('href').encode('utf-8')
                url    = url_base + url
                html   = urllib2.urlopen(url).read()
                soup   = BeautifulSoup(html)

                tabela = soup.find('table',{'class':'dados'})
                for linha in tabela.findAll('tr'):
                    f.write(
                            nome_cidade +
                            '|instituicoes_financeiras|' +
                            linha.findAll('td')[0].get_text() +
                            '|' +
                            linha.findAll('td')[1].get_text().replace('.','').replace(',','.') +
                            '|\n'
                           )
                # -------------------------------------------------------

                # ----- IDHM --------------------------------------------
                busca  = 'idhm'
                url    = soup_Municipio.find('a', href=re.compile(busca)).get('href').encode('utf-8')
                url    = url_base + url
                html   = urllib2.urlopen(url).read()
                soup   = BeautifulSoup(html)

                tabela = soup.find('table',{'class':'dados'})
                for linha in tabela.findAll('tr'):
                    f.write(
                            nome_cidade +
                            '|idhm|' +
                            linha.findAll('td')[0].get_text() +
                            '|' +
                            linha.findAll('td')[1].get_text().replace('.','').replace(',','.') +
                            '|\n'
                           )
                # -------------------------------------------------------

                # ----- Cadastro Central de Empresas --------------------
                busca  = 'tro-central-de-empresas-2013'
                url    = soup_Municipio.find('a', href=re.compile(busca)).get('href').encode('utf-8')
                url    = url_base + url
                html   = urllib2.urlopen(url).read()
                soup   = BeautifulSoup(html)

                tabela = soup.find('table',{'class':'dados'})
                for linha in tabela.findAll('tr'):
                    f.write(
                            nome_cidade +
                            '|cadastro_central_empresas|' +
                            linha.findAll('td')[0].get_text() +
                            '|' +
                            linha.findAll('td')[1].get_text().replace('.','').replace(',','.') +
                            '|\n'
                           )
                # -------------------------------------------------------

                # ----- Censo2010 : Cadastro de Endereços ---------------
                busca  = '2010:-cnefe-cadastro'
                url    = soup_Municipio.find('a', href=re.compile(busca)).get('href').encode('utf-8')
                url    = url_base + url
                html   = urllib2.urlopen(url).read()
                soup   = BeautifulSoup(html)

                tabela = soup.find('table',{'class':'dados'})
                for linha in tabela.findAll('tr'):
                    f.write(
                            nome_cidade +
                            '|cadastro_enderecos|' +
                            linha.findAll('td')[0].get_text() +
                            '|' +
                            linha.findAll('td')[1].get_text().replace('.','').replace(',','.') +
                            '|\n'
                           )
                # -------------------------------------------------------

                # ----- Censo2010 : População ---------------------------
                busca  = 'censo-demografico-2010:-resultados-da-amostra-caracteristicas-da-populacao-'
                url    = soup_Municipio.find('a', href=re.compile(busca)).get('href').encode('utf-8')
                url    = url_base + url
                html   = urllib2.urlopen(url).read()
                soup   = BeautifulSoup(html)

                tabela = soup.find('table',{'class':'dados'})
                for linha in tabela.findAll('tr'):
                    f.write(
                            nome_cidade +
                            '|censo2010_populacao|' +
                            linha.findAll('td')[0].get_text() +
                            '|' +
                            linha.findAll('td')[1].get_text().replace('.','').replace(',','.').replace('-','') +
                            '|\n'
                           )
                # -------------------------------------------------------

                # ----- Censo2010 : Domicílio ---------------------------
                busca  = 'censo-demografico-2010:-resultados-da-amostra-domicilios--'
                url    = soup_Municipio.find('a', href=re.compile(busca)).get('href').encode('utf-8')
                url    = url_base + url
                html   = urllib2.urlopen(url).read()
                soup   = BeautifulSoup(html)

                tabela = soup.find('table',{'class':'dados'})
                for linha in tabela.findAll('tr'):
                    f.write(
                            nome_cidade +
                            '|censo2010_domicilios|' +
                            linha.findAll('td')[0].get_text() +
                            '|' +
                            linha.findAll('td')[1].get_text().replace('.','').replace(',','.').replace('-','') +
                            '|\n'
                           )
                # -------------------------------------------------------

                # ----- Mapa de Pobreza ---------------------------------
                busca  = 'mapa-de-pobreza-e-desigualdade-municipios-brasileiros-2003'
                url    = soup_Municipio.find('a', href=re.compile(busca)).get('href').encode('utf-8')
                url    = url_base + url
                html   = urllib2.urlopen(url).read()
                soup   = BeautifulSoup(html)

                tabela = soup.find('table',{'class':'dados'})
                for linha in tabela.findAll('tr'):
                    f.write(
                            nome_cidade +
                            '|mapa_pobreza_desigualdade|' +
                            linha.findAll('td')[0].get_text() +
                            '|' +
                            linha.findAll('td')[1].get_text().replace('.','').replace(',','.') +
                            '|\n'
                           )
                # -------------------------------------------------------

                # ----- Mapa do Município --- ---------------------------
                #busca  = 'infograficos:-dados-gerais-do-municipio'
                #url    = soup_Municipio.find('a', href=re.compile(busca)).get('href').encode('utf-8')
                #url    = url_base + url
                #html   = urllib2.urlopen(url).read()
                #soup   = BeautifulSoup(html)

                # -------------------------------------------------------
                print nome_cidade + "\t ok!"

f.close()
