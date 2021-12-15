from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd 
import re

# import chromedriver_install as cdi 

header = ['id','title','authorids','authors','TL;DR','abstract','pdf','software','preprint','existing_preprints','preferred_venue','consent','paperhash','reviewer/Editor_reassignment_request','reviewer/Editor_reassignment_justification','data','previous_URL','previous_PDF','response_PDF']

df = pd.DataFrame(columns=header)
# df = df.rename(columns = header)
print(df)

time.sleep(3)
driver = webdriver.Chrome('./chromedriver')
driver.get("https://openreview.net/group?id=aclweb.org/ACL/ARR/2021/November")
time.sleep(3)
html_source = driver.page_source
soup = BeautifulSoup(html_source,'lxml')

ids = dict()
count = 0
print(len(soup.find_all('a')))
for link in soup.find_all("a"):
	addr = link.get('href')
	if addr:
		# print(addr)
		
		temp = re.findall(r"\/(.+?)\?(\w*)(=|&)([a-zA-Z0-9_\-]*)(=|&)*(\w*)(=|&)*(\w*)", str(addr))
		if not temp: 
			continue
		# print(temp[0])
		
		type = temp[0][0]  
		id = temp[0][3]
		# print(id)
		# print(type)

		if type == 'forum': 
			print(type, id)
		elif type =='attachment': 
			name = temp[0][-1]

			print(type, id, name)
			# df.insert(count, 'id', id, name, addr)
		elif type == 'pdf': 
			print(type, id)
			# df.insert(count, 'id', id, 'pdf', addr)

	count+=1 	

		# try:
		# 	type = re.findall(r"\/(.+?)\?", str(addr))[0]
		# 	id = re.findall(r"\?id=(\w*\d*)", str(addr))[0]
		# 	if id and type: 
		# 		print(id, type)
		# 		if id in ids: 
		# 			ids[id].append({type: id})
		# 		else: 
		# 			ids[id] = {type: id}

		# except: 
		# 	continue
		
		
# print(ids)

# ids = dict()
# for link in links: 
# 	id = re.findall(r"/forum\?id=(.+?)\"", str(link))
# 	pdf = re.findall(r"/pdf\?id=(.+?)\"", str(link))
# 	title = link
# 	print(title)
# 	if id:
# 		# print(id)
# 		ids[id[0]] = title

# print(ids)
print(df)