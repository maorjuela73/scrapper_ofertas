from selenium import webdriver
import json
import datetime
from time import sleep
from bs4 import BeautifulSoup
import requests as r



def max_number(driver):
    driver.get('https://www.tuempleord.do/page/{}/'.format(2))
    sleep(1)
    max_number = driver.find_element_by_css_selector('body > div.contenedor > div > div.col-md-8.lista-de-trabajos > div.paginacion > a:nth-child(7)').get_attribute('innerText')
    max_number = int(max_number.replace('.',""))
    print(max_number)
    return(max_number)

def get_lista_empleos(driver , num):
    driver.get('https://www.tuempleord.do/page/{}/'.format(num))
    sleep(1)
    todo_el_html = driver.find_element_by_css_selector('body').get_attribute('innerHTML')
    soup = BeautifulSoup(todo_el_html , 'lxml')
    tags_empleos = soup.findAll('h2' , {'class':'resumido'})

    lista_url_empleos = []
    for i in tags_empleos:
        for j in i:
            lista_url_empleos.append(j['href'])
    return(lista_url_empleos)


def procesar_un_empleo(driver , url_empleo):
    driver.get(url_empleo)
    todo_el_html = driver.find_element_by_css_selector('body').get_attribute('innerHTML')
    soup = BeautifulSoup(todo_el_html , 'lxml')
    titulo = soup.find('h2' , {'class':'titulo-individual'}).getText()
    fecha = soup.find('span' , {'class':'date'}).getText()
    provincia = soup.find('a' , {'class':'pequeno provincia'}).getText()
    categoria = soup.find('a' , {'class':'pequeno categoria'}).getText()
    contenido = soup.findAll('div' , {'class':'contenido'})

    full_content = []
    for i in contenido:
        for j in i:
            full_content.append(j)
    contenido_interesante = (full_content[:-3])

    datos = {
        'fecha':fecha,
        'provincia':provincia,
        'categoria':categoria,
        'titulo':titulo,
        'full_content':str(contenido_interesante),
        'hora_subido':str(datetime.datetime.now())
    }
    return(datos)


driver = webdriver.Chrome()
numero_maximo = max_number(driver)
for i in range(1, numero_maximo):
    lista =  get_lista_empleos(driver , i)
    for k,j in enumerate(lista):
        print("processing ... {}".format(j))
        datos = procesar_un_empleo(driver , j)
        fecha = datetime.datetime.now()
        año = str(fecha.year)
        mes = str(fecha.month)
        dia = str(fecha.day)
        serial = str(((i-1) * 25) + k)
        print(serial)
        print(k,j)
        nombre = f"vacantes/empleord-{año}-{mes}-{dia}-{serial}.json"
        with open(nombre , 'w') as json_file:
            json.dump(datos , json_file)
            sleep(1)

driver.close()




