from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from progress.bar import Bar
import json
from bs4 import BeautifulSoup




#este metodo agarra todas las areas de trabajo y retorna una lista con ellas y su respectivo valor   |jue ene 21 18:07:09 -05 2021|
def get_all_areas(driver):
    driver.get('https://www.tuempleord.do/')
    areas_box = driver.find_element_by_xpath('/html/body/div[3]/div/form/div[1]/select')
    el_html = areas_box.get_attribute('innerHTML')
    sopa  = BeautifulSoup(el_html , 'lxml')
    elementos = sopa.findAll('option')
    areas = []
    for i in elementos:
        for j in i:
            area  = {
                'nombre':j ,
                'value':i['value']
            }
            areas.append(area)

    return(areas)


def scroll(driver):
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except:
        pass


#este metodo agarra todas las provincias y retorna una lista con cada una de ellas   |jue ene 21 18:07:24 -05 2021|
def get_all_provincias(driver):
    driver.get('https://www.tuempleord.do/')
    provincias_box = driver.find_element_by_xpath('/html/body/div[3]/div/form/div[2]/select')
    el_html = provincias_box.get_attribute('innerHTML')
    sopa = BeautifulSoup(el_html , 'lxml')
    elementos = sopa.findAll('option')
    provincias = []
    for i in elementos:
        for j in i:
            provincias.append(j)
    return(provincias)




#dada una secion del paginador   |vie ene 22 10:23:43 -05 2021|
def get_all_vacantes(driver , paginador ):
    driver.get('https://www.tuempleord.do/page/{}/'.format(paginador))
    body = driver.find_element_by_xpath('/html/body').get_attribute('innerHTML')
    soup = BeautifulSoup(body , 'lxml')
    resumidos = soup.findAll('h2' , {'class':'resumido'})

    vacantes = []
    for i in resumidos:
        titulo = i.getText()
#        url = i['href']
        for j in i:
            url = j['href']
        vacante = {
            'titulo':titulo,
            'url':url
        }
        vacantes.append(vacante)
    return(vacantes)


def get_info_vacante(driver, vacante):
    driver.get(vacante['url'])
    contenido = driver.find_element_by_xpath('/html/body/div[8]/div/div[1]/article/div[1]/div[2]')
    html_contenido = contenido.get_attribute('innerHTML')
    soup = BeautifulSoup(html_contenido , 'lxml')
    texto = soup.findAll('p')

    total = {
        'titulo':vacante['titulo'],
        'url':vacante['url']
    }
    for i in texto:
        descripcion = {}
        elemento = i.getText()
        lista = elemento.split('\n')
        try:
            descripcion[lista[0]] = lista[1]
            total[lista[0]] = lista[1]
        except:
            pass
    return(total)





try:
    options = Options()
    options.headless = True
    cont = 1
    driver = webdriver.Chrome(options = options)
    maxi = 1896
    barrita = Bar("progres ..." , max = maxi)
    for i in range(1,maxi):
        vacantes = get_all_vacantes(driver , i)
        for j in vacantes:
            puesto = get_info_vacante(driver , j)
            nombre = 'vacantes/vacante{0:04d}.json'.format(cont)
            cont += 1
            with open(nombre,  'w') as archivo_json:
                json.dump(puesto , archivo_json)

            barrita.next()

    driver.close()
except:
    driver.close()



