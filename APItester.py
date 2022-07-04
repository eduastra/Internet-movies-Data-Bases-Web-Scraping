import sqlite3
import requests
from bs4 import BeautifulSoup
from requests import get
from imdb import IMDb

ia = IMDb()

# Coletar o numero de paginas 
url = requests.get('https://www.imdb.com/search/title?count=100&title_type=feature,tv_series&ref_=nv_wl_img_')
soup = BeautifulSoup(url.text, 'html.parser')

#criando classe de objetos
class IMDB():
    def __init__(self, url):
        super(IMDB, self).__init__()
        soup = BeautifulSoup(url.content, 'lxml')
        self.soup = BeautifulSoup(url.content, 'lxml')
    def articleTitle(self):
        return self.soup.find("h1", class_="header").text.replace("\n","")
    def bodyContent(self):
        content = self.soup.find(id="main")
        return content.find_all("div", class_="lister-item mode-advanced")

#coletando dados
    def DataInsertDB(self):
        Row = 0
        movieFrame = self.bodyContent()
        for movie in movieFrame:
            movieFinder = movie.find("h3", class_="lister-item-header")
            movieTitle = (movieFinder.find("a").text)
            movieDate = (movieFinder.find_all("span")[-1].text)
            movieGenre = (movie.find("span", class_="genre").text.rstrip().replace("\n"\
                ,"").replace("[","").split(","))
            Title = movieTitle
            searchID = ia.search_movie(Title)
            IDmovie = searchID[0].movieID
            movieAPI = ia.get_movie(IDmovie)
            try: #studio
                studio = movieAPI['director'][0:]
            except:
                studio = "none"


#testando objeto
IMDB.DataInsertDB(IMDB(url))

"""
{'main': ['original title', 'localized title', 'cast', 'genres', 'runtimes',
 'countries', 'country codes', 'language codes', 'color info', 'aspect ratio',
'sound mix', 'box office', 'certificates', 'original air date', 'rating', 'votes',
 'cover url', 'imdbID', 'plot outline', 'languages', 'title', 'year', 'kind', 'director',
'writer', 'producer', 'composer', 'cinematographer', 'editor', 'editorial department',
'casting director', 'production design', 'art direction', 'set decoration', 'costume designer',
'make up', 'production manager', 'assistant director', 'art department', 'sound crew',
'special effects', 'visual effects', 'stunt performer', 'camera and electrical department',
'animation department', 'casting department', 'costume department', 'location management',
'music department', 'script department', 'transportation department', 'miscellaneous crew',
 'akas', 'top 250 rank', 'production companies', 'distributors',
'special effects companies', 'other companies'], 'plot': ['plot', 'synopsis']}
"""

