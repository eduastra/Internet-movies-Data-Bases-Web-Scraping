import sqlite3
import requests
from bs4 import BeautifulSoup
from requests import get
from imdb import IMDb

ia = IMDb()

# Coletar o numero de paginas 
url = requests.get('https://www.imdb.com/search/title?count=100&title_type=feature,tv_series&ref_=nv_wl_img_')
soup = BeautifulSoup(url.text, 'html.parser')

pag = soup.find("div", class_="desc").text
url_maker_loop_get = (str(pag)[10:16]).replace(",","")
pagNum = (round(int(url_maker_loop_get)/100))

#começando Banco de dados
conn = sqlite3.connect('test.sqlite')
cur = conn.cursor()
cur.execute('''
DROP TABLE IF EXISTS test''')
cur.execute('''
CREATE TABLE test(ID INT, Title TEXT, OriginalTitle TEXT, Date TEXT, movieGenre TEXT, Studio TEXT)''')

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
                studio = movieAPI['production companies'][0]
            except:
                studio = "none"

            try: #originalMovieTitle
                OriginalMovieTitle = movieAPI['original title']
            except:
                OriginalMovieTitle = "none"

            try: #movieRunTime
                movieRunTime =(movie.find("span", class_="runtime").text[:])
            except:
                movieRunTime = "none"#undisclosed official"/verificar erro

            try: #movieRating
                movieRating = (movie.find("strong").text)
            except:
                movieRating = ("not released")

            try: #movieScore
                movieScore = (movie.find("span", class_="metascore").text.rstrip())
            except:
                movieScore = "nan"
            
            cur.execute('INSERT INTO test (ID, Title, OriginalTitle, Date, movieGenre, Studio\
                ) VALUES (?,?,?,?,?,?\
                    );',(IDmovie,str(movieTitle),str(OriginalMovieTitle),str(movieDate\
                        ),str(movieGenre),str(studio)))

            Row = Row + 1

            cur.fetchone()
            conn.commit()

#testando objeto
IMDB.DataInsertDB(IMDB(url))

#loop de paginas
pag_position = 101
for i in range(pagNum):
    pag_position = pag_position + 100
    new_pag_link = "https://www.imdb.com/search/title/?title_type=feature,tv_series&count=100&start="+str(pag_position)+"&ref_=adv_nxt"