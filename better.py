from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd 
import re


header = ['id','title','authorids','authors','TL;DR','abstract','pdf','software','preprint','existing_preprints','preferred_venue','consent','paperhash','reviewer/Editor_reassignment_request','reviewer/Editor_reassignment_justification','data','previous_URL','previous_PDF','response_PDF']

df = pd.DataFrame(columns=header)
# df = df.rename(columns = header)
print(df)

# time.sleep(3)


driver = webdriver.Chrome('./chromedriver')
driver.get("https://openreview.net/group?id=aclweb.org/ACL/ARR/2021/December")
time.sleep(3)
html_source = driver.page_source
soup = BeautifulSoup(html_source,'lxml')

ids = dict()

find = soup.find_all("li", {"class": "note"})
count = len(find)
for titles in find:
	
	data = dict()

	id = titles.get('data-id')
	if id is None: 
		continue 
	print(id)
	
	h4 = titles.find('h4')
	links = h4.find_all('a')

	title = " ".join(links[0].text.split())
	forum = links[0].get('href')
	pdf = links[1].get('href')
	
	data['id'] = id 
	data['title'] = title
	data['forum'] = forum
	data['pdf'] = forum 
	

	authors = " ".join(titles.find('div', {"class": "note-authors"}).text.split())
	# print(authors)
	data['author'] = authors 

	details = titles.find('ul', {"class": "list-unstyled note-content"})

	items = [" ".join(i.text.split())[:-1] for i in details.find_all('strong', {"class": "note-content-field"})]
	# print(items)
	contents = [" ".join(i.text.split()) for i in details.find_all('span', {"class": "note-content-value"})]
	# print(contents)

	for item, content in zip(items, contents): 
		try: 
			if item != 'Previous URL' and item != 'Abstract':
				t = "Download " + item 
				content = details.find('a', {"title": t}).get('href')
			data[item] = content
		except: 
			pass
	print(data)

	df = df.append(data, ignore_index = True)


	print()

print(df)

print(count)