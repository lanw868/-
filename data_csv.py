#%%
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import csv

prefix = "http://www.shicimingju.com"

#%%
def clean(text):
    text = text.replace('[', '')
    text = text.replace(']', '')
    text = re.sub(r'\([^)]*\)', '', text)
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    text = text.replace(' ', '')
    return text
#%%
def get_poem_url_list(page_url):

	page = urllib.request.urlopen(page_url)
	soup = BeautifulSoup(page, 'lxml')

	h3_tag = soup.find('h3')
#%%
def get_one_poem(poem_url):
	## poem_url = 'http://www.shicimingju.com/chaxun/list/3075402.html'
	page = urllib.request.urlopen(poem_url)
	soup = BeautifulSoup(page, 'lxml')
	# print(soup.prettify())

	## find tags
	title_tag = soup.find('h1', attrs={'class':'shici-title'})
	author_tag = soup.find('div', attrs={'class':'shici-info'}).find('a')
	content_tag = soup.find('div', attrs={'class':'shici-content'})
	mark_tag = soup.find('div', attrs={'class': 'shici-mark'})

	## delete symbols and translate
	title = clean(title_tag.text)
	author = clean(author_tag.text)
	poem = clean(content_tag.text)

	mark = ''
	if mark_tag != None:
		mark_tag = mark_tag.find_all('a')
		for e in mark_tag:
			mark+=(clean(e.text)+'，')
		mark=mark[:-1]

	return (title, author, poem, mark)
#%%
def open_file(filename):
	with open(filename, 'w', newline='', encoding = 'utf-8-sig') as csv_file:
			writer = csv.writer(csv_file)
			# column name
			writer.writerow(["name","author","content","tag"])
#%%
def save_data_to_file(data, filename):
	with open(filename, 'a', newline='', encoding = 'utf-8-sig') as csv_file:
		writer = csv.writer(csv_file)			
		# data
		for title, author, poem, mark in data:
			writer.writerow([title, author, poem, mark])
#%%
def store_page_data(data, page_url):
	page = urllib.request.urlopen(page_url)
	soup = BeautifulSoup(page, 'lxml')

	h3_tag = soup.find_all('h3')

	for h3 in h3_tag:
		poem_url = prefix + h3.find('a').get('href')
		data.append(get_one_poem(poem_url))



author_dict = {
# '李白': [1, 981],'岑參': [3,385], '張九齡': [5,199], '王維': [6,407],'白居易': [8, 2741],
'杜甫': [10,1174], '李商隱': [11,536], '李頎': [140,125], '杜牧': [22,514], '陳子昂': [151,139], 
'高適': [23,205], '王勃': [25,76], '溫庭筠': [27,374], '韓愈': [28,359], '孟浩然': [30,321], 
'孟郊': [31,384], '賀知章': [32,26], '劉禹錫': [42,722], '柳宗元': [50,155], '王之渙': [51,6],
'崔顥': [180,45], '駱賓王': [53,123], '王昌齡': [56,210], '劉長卿': [57,502], '韋應物': [60,549],
'賈島': [62,396]}

url = 'http://www.shicimingju.com/chaxun/zuozhe/{}.html' 
nextPage = 'http://www.shicimingju.com/chaxun/zuozhe/{}_{}.html'

### open_file(filename='./data.csv')

for key in author_dict.keys():
	print('key:',key)
	author_index = author_dict[key][0]
	n_poem = author_dict[key][1]
	n_page = int(np.ceil(n_poem/40))
	for pg in range(1, n_page+1):
		if pg==1:
			page_url = url.format(author_index)
		else:
			page_url = nextPage.format(author_index,pg)

		print('page', pg)

		data=[]
		store_page_data(data, page_url)

		print('page', pg, 'data get')

		save_data_to_file(data, filename='./data.csv')

		print('page', pg,'saved csv')

	print('key:',key, 'done')


