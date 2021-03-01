import requests as r
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver



driver = webdriver.Chrome()

driver.get('http://www.quala.com.do/rep-dominicana-2/empleo-multinacional/ofertas-laborales/')
sleep(5)
puestos = driver.find_element_by_xpath('/html/body/form/div/div/div[2]/div/div[2]/div/div[1]/input[1]')
puestos.click()
sleep(1)
print("buena")
driver.close()




