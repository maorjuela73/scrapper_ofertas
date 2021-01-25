import requests as r
from bs4 import BeautifulSoup


req = r.get('https://quala.taleo.net/careersection/qla_portal_candidatos/jobsearch.ftl?lang=es').content
soup = BeautifulSoup(req, "lxml")
# menus = soup.findAll('div' , {'id':'requisitionListInterface.ID969'})
# menus = soup.select('.inner')
menus = soup.select('.ftllist span a')
print(menus)

for i in menus:
    print(i['href'])


