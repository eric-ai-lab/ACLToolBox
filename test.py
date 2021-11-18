#!/usr/bin/env python
import requests 
from bs4 import BeautifulSoup
import json
import re
import pandas as pd 


months = ['October', 'September', 'August', 'July', 'Jun', 'May']


for month in months:
    print(month)
    URL = "https://openreview.net/group?id=aclweb.org/ACL/ARR/2021/" + month

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

    print(len(title))
    print(len(documents))

    # offset the correct title for each link
    # october [19:-2]
    # september [10:-2]
    # August [10:-2]
    if month == 'October': 
        title = title[19:-2]
    else: 
        title = title[10:-2]

    print(len(title)) 
    print(len(documents))

    # combine the title and documents into dictionary
    database = {}
    for x, y in zip(title, documents): 
        database[x] = y

    # print(database)

    df = pd.DataFrame.from_dict(database, orient='index', columns=['links'])
    print(df)
    df.to_csv(month + '.csv')

