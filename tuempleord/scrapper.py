from selenium import webdriver
import threading
import json
import datetime
import time
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


def scrapear_una_parte( ini , fin):
    options = webdriver.ChromeOptions()
    #options.add_argument('--disable-gpu')
    #options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options = options)
    for i in range(ini, fin):
        lista =  get_lista_empleos(driver , i)
        for k,j in enumerate(lista):
            print("processing ... {}".format(j))
            datos = procesar_un_empleo(driver , j)
            fecha = datetime.datetime.now()
            año = str(fecha.year)
            mes = str(fecha.month)
            dia = str(fecha.day)
            serial = (((i-1) * 25) + k)
            serial = "{0:05d}".format(serial)
            nombre = f"vacantes/empleord-{año}-{mes}-{dia}-{serial}.json"
            with open(nombre , 'w') as json_file:
                json.dump(datos , json_file)
                sleep(1)
    driver.quit()



driver = webdriver.Chrome()
numero_maximo = max_number(driver)
num_pages = max_number(driver)
driver.quit()

num_chunks = 8 # TODO: A calcular de la máquina


def cuts(num_pages, num_chunks):
  amplitude = num_pages//num_chunks + 1
  print(f'amplitude: {amplitude}')
  chunks = [ x for x in range(0,num_pages+1) if x == 0 or x % amplitude == 0 or x == num_pages]
  return chunks


data_cuts = cuts(num_pages, num_chunks)
data_cuts


thread_list = list()


for x , cut in enumerate(data_cuts):
    if (x < len(data_cuts) - 1 ):
        print('Job # ', x + 1 ,[data_cuts[x] + 1 , data_cuts[x+1]])
        t = threading.Thread(name='Test {}'.format(x), target=scrapear_una_parte(data_cuts[x] + 1 , data_cuts[x + 1]))
        t.start()
        time.sleep(1)
        print(t.name + ' started!')
        thread_list.append(t)


# Wait for all threads to complete
for thread in thread_list:
    thread.join()

print('Test completed!')




