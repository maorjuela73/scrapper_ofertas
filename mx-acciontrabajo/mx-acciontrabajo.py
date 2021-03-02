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

def get_urls_empleos(num):

    url='https://acciontrabajo.com.mx/buscar-empleos?p={}'.format(num)

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Selecionamos la porciion del HTLM que contiene todos los empleos de una pagina
    tabla_empleos=soup.find('div','row vhundred hundred')
    #Hacemos una lista separando cada uno de los empleos
    lista_empleos=tabla_empleos.find_all('section')

    #Obtenemos todos los urls de los trabajos de la pagina actual
    urls_empleos=['https://acciontrabajo.com.mx'+urls.a.get('href') for urls in lista_empleos]

    return(urls_empleos)


def data_retrieval(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    #soup = BeautifulSoup(response.content, 'xml')
    soup = BeautifulSoup(response.text, 'html.parser')


    fecha_busqueda = datetime.today().strftime('%Y-%m-%d-%H-%M')

    registro = {
        'url_empleo': url,
        'fecha_recuperacion': fecha_busqueda,
        }


    try:
        empresa=soup.find('b',{'class':"company_under_title"}).get_text(strip=True)
        registro['Empresa']=empresa
    except:
        print('no se recuepro Empresa')
        registro['Empresa']=''

    try:
        vacante=soup.find('div','profile_header_details tal wa').find_next('h1').get_text(strip=True)
        registro['Vacante']=vacante
    except:
        print('no se recuepro vacate')
        registro['Vacante']=''


    #Todos los items
    items=soup.find('div',{'class':'wa mt1 mb1'})
    #Lista de items
    lista_item=items.find_all('div','item_txt')


    try:
        ciudad=lista_item[0].find('span').get_text()
        registro['Ciudad']=ciudad
    except:
        print('no se recuepro ciudad')
        registro['Ciudad']=''

    try:
        estado=lista_item[0].find('a').get_text()
        registro['Estado']=estado
    except:
        print('no se recuepro estado')
        registro['Estado']=''
        
    try:
        experiencia=lista_item[1].next_element.next_element.next_element
        registro['Experiencia']=experiencia
    except:
        print('no se recuepro experiencia')
        registro['Experiencia']=''

    try:
        sector=lista_item[2].next_element.get_text(strip=True)
        registro['Sector']=sector
    except:
        print('no se recuepro sector')
        registro['Sector']=''

    try:
        contrato=lista_item[3].next_element
        registro['Contrato']=contrato
    except:
        print('no se recuepro contrato')
        registro['Contrato']=''
    
    try:
        jornada=lista_item[3].next_element.next_element.next_element
        registro['Jornada']=jornada
    except:
        print('no se recuepro jornada')
        registro['Jornada']=''
    
    try:
        salario=lista_item[4].next_element.next_element.next_element
        registro['Salario']=salario
    except:
        print('no se recuepro salario')
        registro['Salario']=''
    
    try:
        publicado=lista_item[5].next_element.next_element.next_element.next_element.next_element
        registro['Publicado']=publicado
    except:
        print('no se recuepro publicado')
        registro['Publicado']=''


    #Se necesita limpiar los requisitos
    try:
        requisitos=soup.find('div','profile_header_details tal').get_text(strip=True) 
        registro['Requisitos']=requisitos
    except:
        print('no se recuepro requisitos')
        registro['Requisitos']=''
    

    id_job_by_url = re.search("[A-Za-z0-9]*$",url)[0]

    filename = f"acciontrabajo/vacantes/{id_job_by_url}-{fecha_busqueda}.json"

    # Crea la carpeta si no existe
    if not os.path.exists('acciontrabajo/vacantes'):
        os.makedirs('acciontrabajo/vacantes')

    # Crea el archivo a partir del diccionario registro
    with open(filename, 'w') as json_file:
        json.dump(registro, json_file)
        sleep(1)
    
    return(registro)



num=1
while True:
    if len(get_urls_empleos(num))==0:
        print('Se termino la ejecución')
        break
    else:
        urls=get_urls_empleos(num)
        thread_list = list()
        for url in urls:
            t = threading.Thread(name='PROCESSING {}'.format(url), target=data_retrieval, args=(url,))
            thread_list.append(t)
            t.start()
            print(t.name + ' started!')
        for thread in thread_list:
            thread.join()
        print(f'PAGE {num} --- Data retrieval completed!')

        num+=1
