import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import WikiActorMinigUtil
from bs4 import BeautifulSoup


actorPath = "/wiki/Brad_Pitt"
actorName = "Brad Pitt"

soup = WikiActorMinigUtil.getSoup(actorPath)

# Get all Bard Pitt's movies
choosenActorMoviesUrl = WikiActorMinigUtil.getAllMovies(soup, actorName)

#get the movie url and create new soup
movieExtraUrl = WikiActorMinigUtil.getNavigateUrlFromMovieName (soup,"Fight Club")
movieSoup = WikiActorMinigUtil.getSoup(movieExtraUrl)

#find the cast ul to itirate all players in the cast
commonActors = []

# For each actor in this movie, find how many movies he has in common with Brad Pitt's movies
commonMovies = []

actorIndex = 0;
castActors=[]

for movieUrl in choosenActorMoviesUrl :
    #initilize movie page
    movieSoup = WikiActorMinigUtil.getSoup(movieUrl)

    #get all actors from current movie
    print("*** Navigate to: " + movieUrl)
    castActors = WikiActorMinigUtil.getallCastActors(movieSoup)

    for actor in castActors :
        actorIndex = commonActors.index(actor) if actor in commonActors else -1
        if actorIndex == -1 :
            commonActors.append(actor)
            commonMovies.append(1)
        else :
            commonMovies[actorIndex] = commonMovies[actorIndex] + 1



# Create tabel from data
df = pd.DataFrame()
df['Actor'] = commonActors
df['# of common movies'] = commonMovies

print("****")
