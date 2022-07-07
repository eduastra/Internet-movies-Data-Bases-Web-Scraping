import sqlite3
import requests
from bs4 import BeautifulSoup
from requests import get
# Coletar o numero de paginas 
url = requests.get('https://www.imdb.com/search/title?count=100&title_type=feature,tv_series&ref_=nv_wl_img_')
soup = BeautifulSoup(url.text, 'html.parser')

pag = soup.find("div", class_="desc").text
url_maker_loop_get = (str(pag)[10:17]).replace(",","")
pagNum = (round(int(url_maker_loop_get)/100))

#começando Banco de dados
conn = sqlite3.connect('test.sqlite')
cur = conn.cursor()
cur.execute('''
DROP TABLE IF EXISTS test''')
cur.execute('''
CREATE TABLE test(Title TEXT, Date TEXT, Directors TEXT, movieStars TEXT\
    , movieGenre TEXT \
        , movieRating FLOAT, movieRunTime INT, movieDescription TEXT)''')

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
            movieNumbers = movie.find_all("span", attrs={"name": "nv"})
            movieFinder = movie.find("h3", class_="lister-item-header")
            movieTitle = (movieFinder.find("a").text)
            movieDate = (movieFinder.find_all("span")[-1].text)
            try:
                movieGenre = (movie.find("span", class_="genre").text.rstrip().replace("\n"\
                    ,"").replace("[","").split(","))
            except:
                movieGenre = "none"
            movieCast = movie.find("p", class_="")
            Title = movieTitle
            movieNumbers = movie.find_all("span", attrs={"name": "nv"}) 
            try: #movieRating
                movieRating = (movie.find("strong").text)
            except:
                movieRating = ("not released")

            try: #movieRunTime
                if movieRating == "not released":
                    movieRunTime = "not released"
                else:
                    movieRunTime =(movie.find("span", class_="runtime").text[:])
            except:
                movieRunTime = "none"#undisclosed official"/verificar erro

            try: #movieGross
                if len(movieNumbers) == 2:
                    movieGross = movieNumbers[1].text
                elif len(movieNumbers) == 1:
                    movieGross = "not officially disclosed"
                else:
                    if movieRating == "not released":
                        movieGross = "not released"
                    else:
                        movieGross = "none"
            except:
                if movieRating == "not released":
                    movieGross = "not released"

            try:
                casts = movieCast.text.replace("\n","").split('|')
                casts = [x.strip() for x in casts]
                casts = [casts[i].replace(j, "") for i,j in enumerate(["Director:", "Stars:"])]
                movieDirector = (casts[0])
                movieStars = ([x.strip() for x in casts[1].split(",")])
            except:
                casts = movieCast.text.replace("\n","").strip()
                movieDirector = "None"
                movieStars = ([x.strip() for x in casts.split(",")])

            movieDescription = (movie.find_all("p", class_="text-muted")[-1].text.lstrip())

            cur.execute('INSERT INTO test (Title, movieDescription, Date, movieRunTime\
                , movieGenre, movieRating, directors, movieStars \
                ) VALUES (?,?,?,?,?,?,?,?\
                    );',(str(movieTitle), movieDescription ,str(movieDate),str(movieRunTime\
                        ),str(movieGenre),movieRating,str(movieDirector),str(movieStars)))

            Row = Row + 1

            cur.fetchone()
            conn.commit()

#testando objeto na primeira pagina
IMDB.DataInsertDB(IMDB(url))

#testando da segunda em diante

pag_position = 101
for i in range(int(pagNum)):#(20):
    pag_position = pag_position + 100
    new_pag_link = "https://www.imdb.com/search/title/?title_type=feature,tv_series&count=100&start="+str(pag_position)+"&ref_=adv_nxt"
    url = requests.get(new_pag_link)
    soup = BeautifulSoup(url.text, 'html.parser')
    IMDB.DataInsertDB(IMDB(url))
    print(new_pag_link)
