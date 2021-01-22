from selenium import webdriver
from progress.bar import Bar
from time import sleep
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


def get_vacantes(driver , area_value , provincia):
    driver.get('https://www.tuempleord.do/busca-tu-trabajo/?categoria={}&provincia={}'.format(area_value , provincia))
#    driver.get('https://www.tuempleord.do/busca-tu-trabajo/?categoria=17&provincia=haina')
    sleep(1)
    scroll(driver)
    hayalgo = True
    try :
        driver.find_element_by_xpath('/html/body/div[8]/div/div[1]/article[1]/div[2]/div/p')
        hayalgo = True
    except:
        hayalgo = False

    err = 0
    i = 1
    trabajos = []
    while(err < 10):
        try:
            sleep(0.1)
            elemento = driver.find_element_by_xpath('/html/body/div[8]/div/div[1]/article[{}]/div[2]/div/p'.format(i))
            scroll(driver)
            trabajos.append(elemento.get_attribute('innerText'))
            err = 0
            i += 1
        except:
            sleep(0.1)
            err += 1
            i += 1
            pass
    return(trabajos)







driver = webdriver.Chrome()

areas = get_all_areas(driver)
provincias = get_all_provincias(driver)

total = (len(areas) * len(provincias))
barrita = Bar("progress ..." , max=total)
for i in provincias:
    for j in areas:
        vacantes = (get_vacantes(driver , j['value'] , i ))
        if(vacantes != []):
            print(vacantes)
            with open("vacantes/{}_{}_en_{}.json".format(j['value'] , j['nombre'].replace(" ","") , i.replace(" " , "")) , 'w') as vacantejson:
                json.dump(vacantes , vacantejson)
        else:
            with open("vacantes_vacias/{}_{}_en_{}.json".format(j['value'], j['nombre'].replace(" ","") , i.replace(" " , "")) , 'w') as vacantejson:
                json.dump(vacantes , vacantejson)
        barrita.next()


driver.close()


