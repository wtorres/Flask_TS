import urllib2  

from bs4 import BeautifulSoup

from datetime import datetime  
  
quote_page = 'http://www.bloomberg.com/quote/SPGSCITR:IND'

t1 = datetime.now()

page = urllib2.urlopen(quote_page)

soup = BeautifulSoup(page, 'html.parser')

name_store = soup.find('h1', attrs={'class' : 'name'})

data_name = name_store.text.strip()

price_store = soup.find('div', attrs={'class': 'price'})

price = price_store.text

print data_name
print price

t2 = datetime.now()

total = t2 -t1 

print 'scraping completed in ' ,  total


"""
File:ƒcomputesquare.py
Illustratesƒtheƒdefinitionƒofƒaƒmainƒfunction.

def main():
    #Theƒmainƒfunctionƒforƒthisƒscript.
    numberƒ=ƒinput(“Enterƒaƒnumber:ƒ“)
    resultƒ=ƒsquare(number)
    print "The square of,number,ƒ“is”,ƒresult

def square(x):
    “””Returns the square of x.”””
        return x * x

#The entry point for program execution
main()
"""