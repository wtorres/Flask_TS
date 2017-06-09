import urllib2
import requests
from bs4 import BeautifulSoup


quote_page = 'https://www.thestreet.com/markets?cm_ven_int=nav_main'
r = requests.get('https://www.thestreet.com/markets?cm_ven_int=nav_main')


if "blocked" in r.text:
    print "we've been blocked"

print r.status_code

if r.status_code == 200:
    page = urllib2.urlopen(quote_page)

    soup = BeautifulSoup(page, 'html.parser')
    data_name = soup.find('div', attrs={'class' : 'idc-tab-content'})

    print data_name


"""
    for item in data_name.find_all('tr'):
        name_symbol = item.find("u")
        value_symbol = item.find("td", attrs={'nowrap' : "", 'align' : 'right'})
        change = item.find_all("font")

        for i in range(len(change)):
            if i == 1:
                print name_symbol.text, change[i].text

else:
    pass

"""

