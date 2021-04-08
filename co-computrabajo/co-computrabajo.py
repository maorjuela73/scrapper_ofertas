#from selenium import webdriver
import threading
import json
from datetime import datetime
import time
from time import sleep
from bs4 import BeautifulSoup
import os
import requests 
import re
import unicodedata
import math

JOB_OFFERS_PER_PAGE = 20

def get_num_pages():
    url='https://www.computrabajo.com.co/ofertas-de-trabajo/?p={}'.format(1)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    #Retorna urls de las ofertas de trabajo de la pagina
    rango_paginas=soup.find('div','pg_grid')
    num_pages=rango_paginas.find_all('span')[-1].text
    num_pages = int(num_pages.replace('.',""))
    print(f"There are {num_pages} pages to read")
    return(num_pages)

def get_paginator_length(num,dem):
    legt=math.ceil(num/dem)
    return(legt)

def get_urls_empleos(num):

    url='https://www.computrabajo.com.co/ofertas-de-trabajo/?p={}'.format(num)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Retorna urls de las ofertas de trabajo de la pagina
    urls_ofertas=soup.find_all('a','js-o-link')

    #Lista de empleos de la pagina
    lista_url_empleos=['https://www.computrabajo.com.co'+urls.get('href') for urls in urls_ofertas]
    
    return(lista_url_empleos)

def data_retrieval(url):

    fecha_busqueda = datetime.today().strftime('%Y-%m-%d-%H-%M')

    registro = {
        'url_empleo': url,
        'fecha_recuperacion': fecha_busqueda,
    }

    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')

    #Titulo de la oferta
    try:
        titulo_oferta=soup.find('h1' ,{'class':'m0'}).text
        registro['Titulo_oferta']=titulo_oferta
    except:
        registro['Titulo_oferta']=''
        print('no se recupero titulo de la oferta')


    #subitulo de la oferta
    try:
        sub_titulo_oferta= soup.find('span' ,{'class':'fc80 fs14 fl100 fw_n pb10'}).text.strip()
        registro['Subtitulo_oferta']=sub_titulo_oferta
    except:
        registro['Subtitulo_oferta']=''
        print('no se recupero subtitulo de la oferta')

    #Resumen corto
    try:
        short=soup.find('p' ,{'class':'fc80 mt5'}).get_text(strip=True)
        short=re.sub('\r\n +', '', short)
        short = unicodedata.normalize("NFKD",short)
        registro['Informarcion_corta']=short
    except:
        registro['Informarcion_corta']=''
        print('no se recupero informacion corta')


    #empresa
    try:
        emp = soup.find('a' , {'id':'urlverofertas'})
        empresa = emp.getText()
        registro['Empresa']=empresa
    except:
        registro['Empresa']=''
        print('no re recupero empresa')


    #Cuadro de descripcion y requeriminetos
    box1=soup.find('section' ,{'class':'boxWhite fl w_100 detail_of mb20 bWord'})

    #Descripción de la vacante
    try:
        descripcion=descripcion=box1.find('h3' ,{'class':'mt0'}).findNext('li').get_text(strip=True)
        registro['Descripcion']=descripcion
    except:
        registro['Descripcion']=''
        print('no se recupero la descripcion')

    #Requeriminetos
    try:
        requerimientos=''
        for i,l in enumerate(box1.find('ul' ,{'class':'p0 m0'}).find_all('li')):
            if l.get_text(strip=True) == 'Requerimientos':
                z=soup.find('ul' ,{'class':'p0 m0'}).find_all('li')[i+1:-1]
                #print(soup.find('ul' ,{'class':'p0 m0'}).find_all('li')[i+1:-1])
                for j in z:
                    requerimientos+=j.get_text()+', '
        
        registro['Requerimientos']=requerimientos

    except:
        registro['Requerimientos']=''
        print('no se recupero requerimientos')
    
    #Rating empresa
    try:
        url_remp=url+'-empresa'
        req2 = requests.get(url_remp, headers=headers)
        soup2 = BeautifulSoup(req2.text, 'html.parser')

        rating=soup2.find('span','numrate fl mr2').get_text(strip=True)
        registro['Rating']= rating
    except:
        registro['Rating']= ''
        print('No se recupero rating de la empresa')

    #Extrase los datos del resumen
    titulos=soup.find_all('p','fw_b fs15 mt10')
    for i in range(0, len(titulos)):
        if titulos[i].text=='Empresa':
            registro[titulos[i].text] = titulos[0].findNext('a').text.strip()
        else:
            registro[titulos[i].text] = titulos[i].findNext('p').text.strip()


    id_job_by_url = re.search("[A-Z0-9]*$",url)[0]

    filename = f"co-computrabajo/vacantes/{id_job_by_url}-{fecha_busqueda}.json"

    # Crea la carpeta si no existe
    if not os.path.exists('co-computrabajo/vacantes'):
        os.makedirs('co-computrabajo/vacantes')

    # Crea el archivo a partir del diccionario registro
    with open(filename, 'w') as json_file:
        json.dump(registro, json_file)
        sleep(1)
   

    return registro



num_offers = get_num_pages()
num_pages = get_paginator_length(num_offers, JOB_OFFERS_PER_PAGE)


for page in range(1, num_pages+1):
    offers = get_urls_empleos(page)
    thread_list = list()
    for x in offers:
        t = threading.Thread(name='PROCESSING {}'.format(x), target=data_retrieval, args=(x,))
        thread_list.append(t)
        t.start()
        print(t.name + ' started!')
    for thread in thread_list:
        thread.join()
    print(f'PAGE {page} --- Data retrieval completed!')
