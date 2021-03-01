import csv
import os
import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from time import sleep
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import threading


# Retorna los links existentes en una página actual
def get_links(driver):
    soup = BeautifulSoup(driver.page_source, features='lxml')
    cards = soup.find_all('div', {'class': 'result-item'})
    links = [card.find('div','js-area-bind area-bind').get('data-url') for card in cards if card.find('div','js-area-bind area-bind').get('data-url') != ""]
    return links


# Funcion para sacar los datos de una URL
def data_retrieval(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    fecha_busqueda = datetime.today().strftime('%Y-%m-%d-%H-%M')

    registro = {
        'url_empleo': url,
        'fecha_recuperacion': fecha_busqueda,
    }

    # Selecionando la primer 'tarjeta' para obtener data
    offer_data = soup.find('div', 'eeoffer-data-wrapper')

    # Oferta de trabajo
    try:
        oferta = offer_data.find('span', {'class': 'js-jobOffer-title'}).text.strip()
        registro['titulo_oferta']= oferta
    except:
        oferta = ''

    # Salario
    try:
        salario = offer_data.find('span', {'class': 'js-joboffer-salary'}).text.strip()
        registro['salario']= salario

    except:
        salario = ''

    # Ciudad
    try:
        ciudad = offer_data.find('span', {'class': 'js-joboffer-city'}).text.strip()
        registro['ciudad']= ciudad

    except:
        ciudad = ''

    # Fecha de publicacion
    try:
        fecha_publicacion = offer_data.find('span', {'class': 'js-publish-date'}).text.strip()
        registro['fecha_publicacion']= fecha_publicacion
    except:
        fecha_publicacion = ''


    # Area
    try:
        area = offer_data.find('span', {'class': 'js-position-area'}).text.strip()
        registro['area']= area
    except:
        area = ''

    # Numero de vacantes
    try:
        no_vacantes = re.sub(r' +', " ", re.sub(r'[\n\r]', '', offer_data.find('p', {'class': 'js-vacancy'}).text).strip())
        registro['num_vacantes']= no_vacantes
    except:
        no_vacantes = ''

    # Profesion
    try:
        profesion = offer_data.find('span', {'class': 'js-profession'}).text.strip()
        registro['profesion']= profesion
    except:
        profesion = ''

    # Selecionando la segunda 'tarjeta' para obtener data
    description_data = soup.find('div', 'description-block')

    # Descripcion general
    try:
        descripcion_general = description_data.text.strip().replace('\r', '').replace('\n', '')  # .decode('UTF-8')
        registro['descripcion_general'] = descripcion_general
    except:
        descripcion_general = ''

    try:
        additional_data_categ = soup.select_one('i.fa.fa-level-down.fa-fw').next_sibling.next_sibling.text.strip().replace('\r', '').replace('\n', '')
        additional_data_edulevel = soup.select_one('i.fa.fa-graduation-cap.fa-fw').next_sibling.next_sibling.text.strip().replace('\r', '').replace('\n', '')
        additional_data_sector = soup.select_one('i.fa.fa-puzzle-piece.fa-fw').next_sibling.next_sibling.text.strip().replace('\r', '').replace('\n', '')
        additional_data_exp = soup.select_one('i.fa.fa-calendar.fa-fw').next_sibling.next_sibling.text.strip().replace('\r', '').replace('\n', '')
        additional_data_tipocontrato = soup.select_one('i.fa.fa-file-text-o.fa-fw').next_sibling.next_sibling.text.strip().replace('\r', '').replace('\n', '')
        additional_data_idempleo = soup.select_one('i.fa.fa-barcode.fa-fw').next_sibling.next_sibling.text.strip().replace('\r', '').replace('\n', '')

        registro['id_empleo'] = additional_data_idempleo
        registro['categoria'] = additional_data_categ
        registro['nivel_educativo'] = additional_data_edulevel
        registro['sector'] = additional_data_sector
        registro['experiencia'] = additional_data_exp
        registro['tipo_contrato'] = additional_data_tipocontrato
    except:
        print("Hubo un problema buscando algún dato complementario")

    try:
        competencias = [x.text.strip() for x in soup.select_one('.requirements-content').select('span')]
        registro['competencias'] = competencias
    except:
        print("No habían competencias")

    id_job_by_url = re.search("\d+$",url)[0]

    filename = f"co-elempleo/vacantes/{id_job_by_url}-{fecha_busqueda}.json"

    # Crea la carpeta si no existe
    if not os.path.exists('co-elempleo/vacantes'):
        os.makedirs('co-elempleo/vacantes')

    # Crea el archivo a partir del diccionario registro
    with open(filename, 'w') as json_file:
        json.dump(registro, json_file)
        sleep(1)

    return registro


options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# open it, go to a website, and get results
driver = webdriver.Chrome('chromedriver',options=options)

url='https://www.elempleo.com/co/ofertas-empleo/'

driver.get(url)

# Acepta cookies
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'a.btn btn-default submit-politics btnAcceptPolicyNavigationCO'.replace(' ','.')))).click()
# Selecionando para ver de a 100
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'select.form-control js-results-by-page'.replace(' ','.')))).click()
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[8]/div[4]/div[1]/div[4]/div/form/div/select/option[3]'))).click()
# Esperando a que se vaya el spinner
WebDriverWait(driver,10).until_not(EC.visibility_of(driver.find_element_by_css_selector("body > div.text-center.ee-global-spinner-wrapper.js-spinner")))

# Contador de cambios de página
page_before_click = 0

while True:

  soup = BeautifulSoup(driver.page_source, features='lxml')
  # TODO: Espaciones en ee-mod_ y en _active_
  pagination = soup.find('ul', {'class': 'pagination ee-mod'})
  current_page_tag = pagination.find('li',{'class': 'active'})

  current_page = current_page_tag.text.split()[0]

  links = get_links(driver)

  thread_list = list()

  for x in links:
      t = threading.Thread(name='PROCESSING {}'.format(x), target=data_retrieval, args=(x,))
      thread_list.append(t)
      t.start()
      print(t.name + ' started!')

  for thread in thread_list:
      thread.join()

  print(f'PAGE {current_page} --- Data retrieval completed!')

  if page_before_click != current_page:
    page_before_click = current_page
    element = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a.js-btn-next'.replace(' ','.'))))
    element.click()
    WebDriverWait(driver, 10).until_not(EC.visibility_of(driver.find_element_by_css_selector("body > div.text-center.ee-global-spinner-wrapper.js-spinner")))
  else:
    driver.close()
    print(f'se termina el ciclo porque la página enterior {page_before_click} es igual a la actual {current_page}')
    break