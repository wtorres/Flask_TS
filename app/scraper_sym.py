"""
Program: generator.py
Author: Ken
Generates and displays sentences using simple grammar
and vocabulary.Words are chosen at random.
"""

import urllib2
import requests
from bs4 import BeautifulSoup


quote_page = 'http://www.investcom.com/us/mpgnasdaq.htm'
r = requests.get("http://www.investcom.com/us/mpgnasdaq.htm")

if "blocked" in r.text:
    print "we've been blocked"


if r.status_code == 200:
    # Obtener la lista de simbolos del sitio web (quote_page)
    page = urllib2.urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')
    data_name = soup.find('div', attrs={'class' : 'genTable'})

    for item in data_name.find_all('tr'):
        name_symbol = item.find("u")
        value_symbol = item.find("td", attrs={'nowrap' : "", 'align' : 'right'})
        change = item.find_all("font")
        record = {}

        for i in range(len(change)):
            if i == 1:
                record["symbol"] = name_symbol.text
                record["change"] = change[i].text
                #print name_symbol.text, change[i].text
                record = {record["symbol"]:record["change"]}

        print record

else:
    print "Failure of the connection to the web page"
