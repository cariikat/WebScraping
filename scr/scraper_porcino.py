from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

# a queue of urls to be crawled
html = urlopen("https://info.aserca.gob.mx/Porcinos/gp_granja.asp")
bsObj = BeautifulSoup(html.read())
tablepie = bsObj.find_all('table',{'class':'table table-striped'})[0]
rows = tablepie.findAll('tr')
headers = [header.text for header in tablepie.find_all('th')]
rows = []
for row in tablepie.find_all('tr'):
    rows.append([val.text.encode('utf-8').decode('latin') for val in row.find_all('td')])
with open('/Users/carinazavala/Documents/precioEnPie_porcino.csv', 'wt') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(row for row in rows if row)
html = urlopen("https://info.aserca.gob.mx/Porcinos/gp_cortes.asp")
bsObj = BeautifulSoup(html.read())    
tablecortes = bsObj.find_all('table',{'class':'table table-striped'})[0]
rows = tablepie.findAll('tr')
headers = [header.text for header in tablecortes.find_all('th')]
rows = []
for row in tablecortes.find_all('tr'):
    rows.append([val.text.encode('utf-8').decode('latin1') for val in row.find_all('td')])
with open('/Users/carinazavala/Documents/tablecortes.csv', 'wt') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(row for row in rows if row)
