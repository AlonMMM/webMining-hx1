
import urllib2
from bs4 import BeautifulSoup
import pandas as pd

wiki = "https://en.wikipedia.org/wiki/Brad_Pitt_filmography"
page = urllib2.urlopen(wiki)
soup = BeautifulSoup(page)

filmsTable = soup.find('table', class_= "wikitable sortable plainrowheaders")

titles = []
years = []
roles = []

for row in filmsTable.findAll('tr'):
    titleCells = row.find('th')
    infoCells = row.findAll('td')
    if(len(infoCells)==6 ):
        years.append(infoCells[0].find(text=True))

        if (len(titleCells.findAll('span')) > 0):
            titles.append(titleCells.findAll('span')[1].find(text=True))
        else:
            titles.append(titleCells.find(text=True))

        if(len(infoCells[3].findAll('span')) > 0) :
            roles.append(infoCells[3].findAll('span')[1].find(text=True))
        else :
            roles.append(infoCells[3].find(text=True))

#Create tabel from data
df=pd.DataFrame()
df['Title'] = titles
df['Year'] = years
df['Role'] = roles

df


print("****")


