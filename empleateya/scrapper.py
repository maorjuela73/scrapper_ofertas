from selenium import webdriver
import json
from time import sleep



def guardar(vacante , num):
    nombre = 'vacantes/vacante_{0:04d}.json'.format(num)
    with open(nombre, 'w') as archivo_json:
        json.dump(vacante , archivo_json)

driver = webdriver.Chrome()

cont = 1
err = 0
total = 0

driver.get('http://empleateya.mt.gob.do/#/empleo/buscar-empleo')

total = 0
for j in range(0,10):
    for i in range(1,7):
        print(i)
        elem = driver.find_element_by_xpath('/html/body/app-root/app-buscar-empleo/main/article/section[1]/article[2]/div/div[{}]/div[2]'.format(i))
        elem.click()

        caja = driver.find_element_by_xpath('/html/body/app-root/app-buscar-empleo/main/article/section[1]/article[2]/div/div[8]')
        caja_html =  caja.get_attribute('innerText')
        empleo = caja_html
        guardar(empleo , total)
        afuera = driver.find_element_by_xpath('/html/body/app-root/app-buscar-empleo/main/article/section[1]/article[2]/div/div[8]/section[1]/span')
        afuera.click()
        total += 1
        print(total)
        sleep(0.3)

    next_button = driver.find_element_by_xpath('/html/body/app-root/app-buscar-empleo/main/article/section[2]/div[13]/button')
    next_button.click()
    sleep(0.5)


driver.close()


