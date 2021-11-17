#!/usr/bin/env python
import requests 
from bs4 import BeautifulSoup
import json
import re


URL = "https://openreview.net/group?id=aclweb.org/ACL/ARR/2021/November"

# get the page by senting request 
page = requests.get(URL)

# beautifulSoup by using lxml to get the raw html and store in soup with different class 
soup = BeautifulSoup(page.content, "lxml")

# find the script that contains the json data
script = soup.find("script", id="__NEXT_DATA__")

# loading the script into json format
json_object = json.loads(script.string)

# using regex for parsing the link of each paper
documents = re.findall(r"<li><a href=\\\\\"(.+?)\\\\\"", str(json_object['props']))

# using regex for parsing the title of each paper
title = re.findall(r"\">(.+?)<", str(json_object['props']))

# offset the correct title for each link
title = title[10:-2]

# combine the title and documents into dictionary
database = {}
for x, y in zip(title, documents): 
    database[x] = y

print(database)
