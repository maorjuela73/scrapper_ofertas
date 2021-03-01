from selenium import webdriver
import threading
import json
import datetime
import time
from time import sleep
from bs4 import BeautifulSoup
import os
import pandas as pd

def get_num_pages(driver):
    driver.get('https://www.tuempleord.do/page/{}/'.format(2))
    sleep(1)
    num_pages = driver.find_element_by_css_selector('body > div.contenedor > div > div.col-md-8.lista-de-trabajos > div.paginacion > a:nth-child(7)').get_attribute('innerText')
    num_pages = int(num_pages.replace('.',""))
    print(f"There are {num_pages} pages to read")
    return(num_pages)


def get_urls_empleos(driver , num):
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


def procesar_url_empleo(driver , url_empleo):
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


def procesar_bloque(df_resultados, pag_inicial , pag_final):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options = options)
    for i in range(pag_inicial, pag_final):
        lista =  get_urls_empleos(driver , i)
        for k,j in enumerate(lista):
            print("processing ... {}".format(j))
            datos = procesar_url_empleo(driver , j)
            fecha = datetime.datetime.now()
            anio = str(fecha.year)
            mes = str(fecha.month)
            dia = str(fecha.day)
            serial = (((i-1) * 25) + k)
            serial = "{0:05d}".format(serial)
            nombre = f"tuempleord/vacantes/tuempleord_{anio}-{mes}-{dia}_pag{i}-emp{k+1}.json"

            if not os.path.exists('tuempleord/vacantes'):
                os.makedirs('tuempleord/vacantes')

            with open(nombre , 'w') as json_file:
                json.dump(datos , json_file)
                sleep(1)

            global df_ofertas
            df_ofertas = df_resultados.append(datos, ignore_index=True)

    driver.quit()


def cuts(num_pages, num_chunks):
  amplitude = num_pages//num_chunks + 1
  print(f'amplitude: {amplitude}')
  chunks = [ x for x in range(0,num_pages+1) if x == 0 or x % amplitude == 0 or x == num_pages]
  return chunks


options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)
num_pages = get_num_pages(driver)
driver.quit()

num_chunks = 2 # TODO: A calcular de la máquina
data_cuts = cuts(num_pages, num_chunks)
df_ofertas = pd.DataFrame(columns=['fecha', 'provincia', 'categoria', 'titulo', 'full_content', 'hora_subido'])

thread_list = list()

for x , cut in enumerate(data_cuts):
    if (x < len(data_cuts) - 1 ):
        print('Job # ', x + 1 ,[data_cuts[x] + 1 , data_cuts[x+1]])
        t = threading.Thread(name='Test {}'.format(x), target=procesar_bloque, args=(df_ofertas, data_cuts[x] + 1 , data_cuts[x + 1], ) )
        thread_list.append(t)
        t.start()
        print(t.name + ' started!')


for x , cut in enumerate(data_cuts):
    if (x < len(data_cuts) - 1 ):
        print('Job # ', x + 1 ,[data_cuts[x] + 1 , data_cuts[x+1]])


# Wait for all threads to complete
for thread in thread_list:
    thread.join()

print('Data retrieval completed!')
