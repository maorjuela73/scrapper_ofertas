from selenium import webdriver
import datetime
import json
from time import sleep



def grab_ultimo(driver):
    driver.get('http://empleateya.mt.gob.do/#/empleo/buscar-empleo')
    sleep(1)
    ultimo_button = driver.find_element_by_xpath('/html/body/app-root/app-buscar-empleo/main/article/section[2]/div[14]/button').click()
    sleep(0.5)
    ultima_pagina = driver.find_element_by_xpath('/html/body/app-root/app-buscar-empleo/main/article/section[2]/div[12]/button').get_attribute('innerText')
    return(int(ultima_pagina))



def guardar(vacante , num):
    nombre = 'vacantes/vacante_{0:03d}.json'.format(num)
    with open(nombre, 'w') as archivo_json:
        json.dump(vacante , archivo_json)

driver = webdriver.Chrome()

cont = 1
err = 0
total = 1

ultimo = grab_ultimo(driver)
driver.get('http://empleateya.mt.gob.do/#/empleo/buscar-empleo')


print("hay {} paginas".format(ultimo))
total = 1
for j in range(0,ultimo):
    sleep(1)
    try:
        for i in range(1,7):
            print(i)
            elem = driver.find_element_by_xpath('/html/body/app-root/app-buscar-empleo/main/article/section[1]/article[2]/div/div[{}]/div[2]'.format(i))
            nombre_box = driver.find_element_by_xpath('/html/body/app-root/app-buscar-empleo/main/article/section[1]/article[2]/div/div[{}]/div[2]/h3'.format(i))
            nombre = nombre_box.get_attribute('innerText')
            try:
                provincia_box = driver.find_element_by_xpath('/html/body/app-root/app-buscar-empleo/main/article/section[1]/article[2]/div/div[{}]/div[2]/ul/li[1]'.format(i))
                provincia = provincia_box.get_attribute('innerText')
                provincia = provincia.replace("Provincia:" ,"")
            except:
                provincia = "no especificado"
            try:
                jornada_box = driver.find_element_by_xpath('/html/body/app-root/app-buscar-empleo/main/article/section[1]/article[2]/div/div[{}]/div[2]/ul/li[2]'.format(i))
                jornada = jornada_box.get_attribute('innerText')
                jornada = jornada.replace('Jornada:' , "")
                if(jornada ==""):
                    jornada = "no especificada"
            except:
                jornada = "no especificada"
            try:
                salario_box = driver.find_element_by_xpath('/html/body/app-root/app-buscar-empleo/main/article/section[1]/article[2]/div/div[{}]/div[2]/ul/li[3]'.format(i))
                salario = salario_box.get_attribute('innerText')
                salario = salario.replace("Salario:" , "")
            except:
                salario = 'no especificado'
            print(nombre , provincia , jornada , salario)
            elem.click()

            caja = driver.find_element_by_xpath('/html/body/app-root/app-buscar-empleo/main/article/section[1]/article[2]/div/div[8]')
            caja_html =  caja.get_attribute('innerText')
            empleo = {
                'nombre_empleo':nombre,
                'provincia':provincia,
                'jornada':jornada,
                'salario':salario,
                'descripcion_completa':caja_html,
                'hora_scrapeada':str(datetime.datetime.now())
            }
            guardar(empleo , total)
            afuera = driver.find_element_by_xpath('/html/body/app-root/app-buscar-empleo/main/article/section[1]/article[2]/div/div[8]/section[1]/span')
            afuera.click()
            total += 1
            print(total)
            sleep(0.3)

        next_button = driver.find_element_by_xpath('/html/body/app-root/app-buscar-empleo/main/article/section[2]/div[13]/button')
        next_button.click()
        sleep(0.5)
    except:
        print("no hay mas empleo")
        break


print('done')
driver.close()


