#!/usr/bin/env python
import requests 
from bs4 import BeautifulSoup
import json
import re
URL = "https://openreview.net/group?id=aclweb.org/ACL/ARR/2021/November"

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# links = soup.find(class="container") 

script = soup.find("script", id="__NEXT_DATA__")
# print(str(script.string))
json_object = json.loads(script.string)

# print(json_object['props'])

# test = BeautifulSoup(json_object['props'], "html.parser")
documents = re.findall(r"<li><a href=\\\\\"(.+?)\\\\\"", str(json_object['props']))
title = re.findall(r"\">(.+?)<", str(json_object['props']))
title = title[10:-2]
print(len(documents))
print(len(title))

database = {}
for x, y in zip(title, documents): 
    database[x] = y

print(database)
