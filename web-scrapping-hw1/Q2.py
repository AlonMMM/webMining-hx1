import urllib2
from bs4 import BeautifulSoup
import pandas as pd


def parseCountry(country):
    if (',' in country) :
        country = country.split(',')[1]
    return country


wiki = "https://en.wikipedia.org"
actor = "/wiki/Brad_Pitt_filmography"
page = urllib2.urlopen(wiki + actor)
soup = BeautifulSoup(page)

filmsTable = soup.find('table', class_="wikitable sortable plainrowheaders")

titleRef = filmsTable.findAll('tr')[2].find('th').find('a').get("href")
wikiNewLink = wiki + titleRef

page = urllib2.urlopen(wikiNewLink)
soup = BeautifulSoup(page)

cast = soup.findAll('ul')[1]

names = []
years = []
countries = []
awards = []

for li in cast.findAll('li'):
    wikiActorPage = wiki + li.find('a').get('href')
    print("**Try navigate to URL : " + wikiActorPage)
    if ("page does not exist" in li.find('a').get('title') or "Brad Pitt" in li.find('a').get('title')):
        print("Navigation stopped")
        continue
    page = urllib2.urlopen(wikiActorPage)
    soup = BeautifulSoup(page)
    print("Navigation succeeded")
    actorInfo = soup.findAll('table', class_="infobox biography vcard")
    if (len(actorInfo) > 0):
        names.append(actorInfo[0].find('span', class_='fn').find(text=True))
        years.append(actorInfo[0].find('span', class_='bday').find(text=True).split('-')[0])
        countries.append(parseCountry((actorInfo[0].find('span', class_='birthplace').findAll(text=True))[-1]))

# Create tabel from data
df = pd.DataFrame()
df['Name'] = names
df['Year'] = years
df['Country'] = countries

print("****")


