import base64
import datetime
from selenium import webdriver
import json
import requests as r
from time import sleep
from bs4 import BeautifulSoup


def get_ofertas(driver, paginador):
    driver.get('https://www.computrabajo.com.do/ofertas-de-trabajo/?p={}'.format(paginador))
    body_html = driver.find_element_by_xpath('/html/body/div[1]/section').get_attribute('innerHTML')
    soup = BeautifulSoup(body_html  , 'lxml')
    elementos = soup.findAll('a' , {'class':'js-o-link'})
    links = []
    for i in elementos:
        link = 'https://www.computrabajo.com.do/' + i['href']
        links.append(link)
    return(links)


def get_info_url(url):
    req = r.get(url).content
    soup = BeautifulSoup(req , 'lxml')
    caja = soup.findAll('ul' ,{'class':'p0 m0'})
    tit = soup.find('h1' ,{'class':'m0'})
    desc = soup.find('ul' ,{'class':'p0 m0'})
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

    titulo = (tit.getText())
    array = []
    for i in desc:
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


#def get_info(driver , link):
    #driver.get(link)
    #sleep(1)
    #nombre_box = driver.find_element_by_xpath('/html/body/div[2]/div[2]/article/div[1]/div[1]/h1')
    #nombre = nombre_box.get_attribute('innerText')
    #description_box = driver.find_element_by_xpath('/html/body/div[2]/div[3]/article[1]/section[1]/ul/li[2]')
    #description = description_box.get_attribute('innerText')

    #req1 = driver.find_element_by_xpath('/html/body/div[2]/div[3]/article[1]/section[1]/ul/li[4]')
    #idiomas = driver.find_element_by_xpath('/html/body/div[2]/div[3]/article[1]/section[1]/ul/li[5]').get_attribute('innerText')
    #edad = driver.find_element_by_xpath('/html/body/div[2]/div[3]/article[1]/section[1]/ul/li[6]').get_attribute('innerText')
    #disponibilidad_viaje = driver.find_element_by_xpath('/html/body/div[2]/div[3]/article[1]/section[1]/ul/li[7]').get_attribute('innerText')
    #cambio_resistencia = driver.find_element_by_xpath('/html/body/div[2]/div[3]/article[1]/section[1]/ul/li[8]').get_attribute('innerText')
    #educacion = (req1.get_attribute('innerText'))

    #info = {
    #    'nombre':nombre,
    #    'descripcion':description,
    #    'educacion':educacion,
    #    'idiomas':idiomas,
    #    'disponibilidad para viajar':disponibilidad_viaje,
    #    'disponibilidad de cambio de residencia':cambio_resistencia
    #}
    #return(info)



#MAIN   |vie ene 22 14:57:42 -05 2021|

driver = webdriver.Chrome()
err = 0
i = 1
cont = 0
while(err < 10):
    try:
        ofertas = get_ofertas(driver , i)
        i+=1
        for j in ofertas:
            nombre = 'vacantes/vacante_{0:05d}.json'.format(cont)
            info = get_info_url(j)
            with open(nombre , 'w') as json_file:
                json.dump(info , json_file)
                print("saved")
            cont += 1
            print(cont)
        err = 0
    except:
        print("error" , err)
        err += 1
        i += 1
        cont += 1



driver.close()

