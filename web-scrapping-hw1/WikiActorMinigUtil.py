import urllib2
from bs4 import BeautifulSoup
import pandas as pd

def getSoup(extraPath) :
    try :
        wiki = "https://en.wikipedia.org"
        page = urllib2.urlopen(wiki + extraPath)
        soup = BeautifulSoup(page)
        return soup
    except Exception :
        return "page does not exist"



def getAllMovies(soup,actorName):
    movies = []
    filmography = soup.find('span', {"id": "Filmography"})
    if(filmography is None) :
        #check if can navigate to filmography page
        soup = getSoup("/wiki/"+actorName.replace(" ","_") + "_filmography")
        if(soup is not "page does not exist") :
            movies = getAllMoviesFromTable(soup.find(class_="wikitable"))
        else :
            return movies
    else :
        filmographyNavigation = filmography.findNext('a').find(text=actorName + " filmography")
        if filmographyNavigation is not None :
            #actor have ref to saparate page for his filmography
            soup = getSoup("/wiki/"+filmographyNavigation.replace(" ","_") + "_filmography")
            movies = getAllMoviesFromTable(soup)
        elif filmography.findNext(class_="wikitable") :
            movies = getAllMoviesFromTable(filmography)
        else :
            movies=getAllMoviesList(filmography)

    return movies

def getAllMoviesFromTable(filmsTable) :
    movies = []
    #in each table the title locate diffrent - find the location of the title
    tableHead = filmsTable.findAll('th')
    titleIndex = 0
    for th in tableHead :
        if not th.find(text="Title")is None :
             break
        titleIndex=titleIndex+1

    for row in filmsTable.findAll('tr') :
         infoCells = row.findAll('i')
         if (len(infoCells)>0):
             movieUrl = infoCells[0].find('a')
             if (movieUrl is not None):
                 movies.append(movieUrl.get('href'))

    return movies

def getAllMoviesList(filmography):
    movies = []
    for ul in filmography.findNext("ul"):
        if (len(ul.findAll("i"))>0):
            for i in ul.findAll("i"):
                movieUrl = i.find('a')
                if(movieUrl is not None) :
                    movies.append(movieUrl.get('href'))

    return movies

def getNavigateUrlFromMovieName(soup,movieName) :
    return soup.find('a',text=movieName).get('href')


def getActorsFromTable(actorTable):
    actors = []
    for row in actorTable.findAll('tr'):
         infoCells = row.findAll('td')
         if (len(infoCells)>0):
             actors.append(infoCells[0].find(text=True))

    return actors

def getActorsFromUl(castsoup):
    actors= []
    actorsLi = castsoup.findAll('li')
    for li in actorsLi :
        actors.append(li.find(text=True))

    return actors


def collectHTMLtextBetweenTags(castTag,tagToBreak):
    html = u""
    for tag in castTag.next_siblings:
        if tag.name == tagToBreak:
            break
        else:
            html += unicode(tag)
    return html


def getallCastActors(movieSoup) :
    actors = []

    if(movieSoup.find('span', {"id": "Cast"}) is  None) :
        return actors

    #finding the cast area in the page
    castTag = movieSoup.find('span', {"id": "Cast"}).next_siblings

    #collect text beween tow tags (need to collect until got another h2)
    castTag = collectHTMLtextBetweenTags(castTag,"h2")

    castTable = movieSoup.find('span', {"id": "Cast"}).findNext(class_="wikitable")
    if(castTable is not None) :
        actors=getActorsFromTable(castTable)
    else :
        castUl = movieSoup.find('span', {"id": "Cast"}).findNext('ul')
        actors=getActorsFromUl(castUl)

    return actors