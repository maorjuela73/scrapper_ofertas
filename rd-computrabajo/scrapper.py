from selenium import webdriver
from bs4 import BeautifulSoup
import requests as r
import datetime
import json
import math
import threading


JOB_OFFERS_PER_PAGE = 20


def get_offers_in_page(driver, page):
    driver.get('https://www.computrabajo.com.do/ofertas-de-trabajo/?p={}'.format(page))
    body_html = driver.find_element_by_xpath('/html/body/div[1]/section').get_attribute('innerHTML')
    soup = BeautifulSoup(body_html  , 'lxml')
    elementos = soup.findAll('a' , {'class':'js-o-link'})
    links = []
    for i in elementos:
        link = 'https://www.computrabajo.com.do/' + i['href']
        links.append(link)
    return(links)


def get_num_offers(driver):
    driver.get('https://www.computrabajo.com.do/ofertas-de-trabajo/')
    soup = BeautifulSoup(driver.page_source, features='lxml')
    return int(soup.find('div', {'class':'breadtitle_mvl'}).span.string)


def get_paginator_length(num_offers, offers_per_page):
    return math.ceil(num_offers / offers_per_page)


def data_retrieval(url):
    req = r.get(url).content
    soup = BeautifulSoup(req , 'lxml')
    caja = soup.findAll('section' ,{'class':'boxWhite fl w_100 ocultar_mvl p30'})
    offer_title = soup.find('h1' ,{'class':'m0'})
    offer_desc = soup.find('ul' ,{'class':'p0 m0'})
    header = soup.find('p' , {"class":'fc80 mt5'})
    texto = header.getText()
    texto = texto.split('\n')
    emp = soup.find('a' , {'id':'urlverofertas'})
    empresa = emp.getText()
    url_empresa = emp['href']
    url_empresa = 'https://www.computrabajo.com.do/' + url_empresa
    algo =1
    if(len(texto) == 7):
        salario = texto[1]
        region = texto[3]
        ciudad = texto[4]
        hora = texto[5]
    else:
        salario = "no especificado"
        region = texto[2]
        ciudad = texto[3]
        hora = texto[4]

    #salario = salario.strip()
    #region = region.replace("  ", "")
    #ciudad = ciudad.replace("  ", "")
    #hora = hora.replace("  ", "")
    salario = ("salario"  , str(salario).strip())
    region = ("region " , str(region).strip())
    ciudad = ("ciudad" , str(ciudad).strip())
    hora = ("hora" , str(hora).strip())
    salario = salario[1]
    region = region[1]
    ciudad = ciudad[1]
    hora = hora[1]

    titulo = (offer_title.getText())
    array = []
    for i in offer_desc:
        array.append(str(i))
    #codifique esta vuelta en base64 para poderlo subir como json   |vie ene 22 16:12:01 -05 2021
    info = {
        'url_de_la_empresa':url_empresa,
        'empresa':empresa,
        'url_de_la_vacante':url,
        'titulo':titulo,
        'descripcion':array,
        'fecha agregado':str(datetime.datetime.now()),
        'salario':salario,
        'region':region,
        "ciudad":ciudad,
        'hora':hora
    }
    return(info)


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome('chromedriver',options=options)

num_offers = get_num_offers(driver)
num_pages = get_paginator_length(num_offers, JOB_OFFERS_PER_PAGE)

for page in range(1, num_pages+1):
    offers = get_offers_in_page(driver, page)
    thread_list = list()
    for x in offers:
        t = threading.Thread(name='PROCESSING {}'.format(x), target=data_retrieval, args=(x,))
        thread_list.append(t)
        t.start()
        print(t.name + ' started!')
    for thread in thread_list:
        thread.join()
    print(f'PAGE {page} --- Data retrieval completed!')


offers = get_offers_in_page(driver , page)
url = offers[0]

#
# err = 0
# i = 1
# cont = 0
# while(err < 10):
#     try:
#         ofertas = get_ofertas(driver , i)
#         i+=1
#         for j in ofertas:
#             nombre = 'vacantes/vacante_{0:05d}.json'.format(cont)
#             info = get_info_url(j)
#             with open(nombre , 'w') as json_file:
#                 json.dump(info , json_file)
#                 print("saved")
#             cont += 1
#             print(cont)
#         err = 0
#     except:
#         err += 1
#         i += 1
#         cont +=1
#         print("error" , err)



driver.close()

