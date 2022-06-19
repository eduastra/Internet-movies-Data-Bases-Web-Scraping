from posixpath import split
import lxml
import re
from matplotlib.pyplot import connect
import numpy as np
import pandas as pd
import sqlite3

from bs4 import BeautifulSoup
from requests import get

url1 = "https://www.imdb.com/search/title?count=100&title_type=feature,tv_series&ref_=nv_wl_img_2"

conn = sqlite3.connect('IMDataBase.sqlite')
cur = conn.cursor()

cur.execute('''
DROP TABLE IF EXISTS films''')

cur.execute('''
CREATE TABLE films( id INTEGER, movieTitle TEXT, movieDate TEXT, movieRunTime TEXT, movieGenre TEXT,
 movieRating TEXT, movieScore TEXT, movieDescription TEXT, movieDirector TEXT, movieStars TEXT,
  movieVotes TEXT, movieGross TEXT)''')

class IMDB():
	def __init__(self, url):
		super(IMDB, self).__init__()
		page = get(url)

		self.soup = BeautifulSoup(page.content, 'lxml')

	def articleTitle(self):
		return self.soup.find("h1", class_="header").text.replace("\n","")

	def bodyContent(self):
		content = self.soup.find(id="main")
		return content.find_all("div", class_="lister-item mode-advanced")

	def movieData(self):
		movieFrame = self.bodyContent()
		movieTitle = []
		for movie in movieFrame:
			movieFirstLine = movie.find("h3", class_="lister-item-header")
			movieTitle.append(movieFirstLine.find("a").text)
		return movieTitle

x=IMDB.movieData(IMDB(url1))
a=x[0]
b=x[1]
c=x[2]
d=x[3]
e=x[4]
f=x[5]
g=x[6]
i=x[7]
j=x[8]
k=x[9]
l=x[10]
m=x[11]

print(x[3])

"""
for i in range(len(x)):

	cur.execute('INSERT INTO films (id, movieTitle) VALUES (?,?)', (i,x[i],))
#	cur.execute('INSERT INTO films (id) VALUES (?)', (i,))
#criar variavel codificadas dentro do loop i e no final do loop i+1 dar um commit para todas variaveis entrarem no sql de uma forma só 
cur.fetchone()
conn.commit()
"""