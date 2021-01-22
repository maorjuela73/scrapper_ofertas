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

    titulo = (tit.getText())
    descripcion = desc
    info = {
        'titulo':titulo,
        'descripcion':desc
    }

    return(info)


#esta verga funcionaba pero dejó de funcionar entonces estoy viendo que pasa   |vie ene 22 15:08:06 -05 2021|
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
while(err < 10):
    nombre = 'vacantes/vacante_{}.json'.format(i)
    ofertas = get_ofertas(driver , i)
    i+=1
    for j in ofertas:
        info = get_info_url(j)
        print(info)
        #with open(nombre , 'w') as json_file:
        #    json.dump(info , json_file)
        #print(i)
    err = 0



driver.close()

