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
CREATE TABLE films( movieTitle TEXT, movieDate TEXT, movieRunTime TEXT, movieGenre TEXT,
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
			print(movieFirstLine)
			with open('arq01.txt', 'w') as arquivo:
				print(movieFirstLine.text)

X = IMDB.movieData(IMDB(url1))
X	

#with open("base.txt", "w") as external_file:
#	add_text = print(IMDB.movieData(IMDB(url1)))
#	print(add_text, file=external_file)
#	external_file.close()
#
#			with open('base.txt', 'w') as f:
#				f.write(print(movieFirstLine.text))
#			movieTitle.append(movieFirstLine.find("a").text)
#			cur.execute('''INSERT INTO films (movieTitle) VALUES (?)''', (str))
#			cur.fetchone()
#			conn.commit()
		
#IMDB.movieData(IMDB(url1))

#with open('base.txt', 'w') as f:
#	f.write(IMDB.movieData(IMDB(url1)))