#!/usr/bin/env python
from pandas.core.frame import DataFrame
import requests 
from bs4 import BeautifulSoup
import json
import re
import pandas as pd 

dir = 'csv/'
# June is written as Jun on website 
months = ['November', 'October', 'September', 'August', 'July', 'Jun', 'May']



url = "https://openreview.net/group?id=aclweb.org/ACL/ARR/2021/" 
forum = 'https://openreview.net/forum?id='
pdf = 'https://openreview.net/pdf?id=' 

print('Starting scraping the data...')
for month in months:
    # print(month)
    URL = url + month

    # get the page by senting request 
    main_page = requests.get(URL)

    # beautifulSoup by using lxml to get the raw html and store in soup with different class 
    soup = BeautifulSoup(main_page.content, "lxml")

    # find the script that contains the json data
    script = soup.find("script", id="__NEXT_DATA__")

    # loading the script into json format
    json_object = json.loads(script.string)

    # using regex for parsing the id of each paper
    ids = re.findall(r"forum\?id=(.+?)\\", str(json_object['props']))
    data = []
    big_json = {}
    for id in ids: 
        # print(id)
        page = requests.get(forum+id)
        soup = BeautifulSoup(page.content, "lxml")
        script = soup.find("script", id="__NEXT_DATA__")

        # loading the script into json format
        json_object = json.loads(script.string)
        # print(json_object)
        # data = json_object['props']['pageProps']['forumNote']
        data = None 
        if 'forumNote' in json_object['props']['pageProps']: 
            data=json_object['props']['pageProps']['forumNote']['content']
        big_json[id] = data
        

    # big_json = json.dumps(big_json)
    df = pd.DataFrame.from_dict(big_json)
    df = df.swapaxes("index", "columns")
    df = df.rename(columns={'Unnamed: 0': 'id'})
    # print(df)
    df.to_csv(dir + month + '.csv')
    print('Data have saved in the ' + dir )
  
