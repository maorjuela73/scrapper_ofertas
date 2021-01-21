from selenium import webdriver
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
                'valor':i['value']
            }
            areas.append(area)

    return(areas)

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


driver = webdriver.Chrome()

areas = get_all_areas(driver)
provincias = get_all_provincias(driver)
print(areas)
driver.close()


