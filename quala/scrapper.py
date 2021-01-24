import requests as r
from bs4 import BeautifulSoup




req = r.get('http://www.quala.com.do/rep-dominicana-2/empleo-multinacional/ofertas-laborales/').content
soup = BeautifulSoup(req , 'lxml')
menus = soup.findAll('ul' , {'class':'menu'})

print(menus)
