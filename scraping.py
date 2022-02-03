#!/usr/bin/env python
from pandas.core.frame import DataFrame
import requests 
from bs4 import BeautifulSoup
import json
import re
import pandas as pd 

from library import * 


dir = 'database/'
file_type = '.csv'


url = "https://openreview.net/group?id=aclweb.org/ACL/ARR" 
forum = 'https://openreview.net/forum?id='

years = []

print('Starting scraping the data...')
# months = {11:'November', 12:'December'}
# years = {2021:'2021', 2022:'2022'}
page = requests.get(url) 
if not page: 
    print('404 not find')
else: 
    years = get_ids_from_page(page, 'year')

for year in years: 

    URL = url + '/' +year
    page = requests.get(URL)
    if not page: 
        print('no ' + year) 
        continue

    months = get_ids_from_page(page, 'month')

    path = os.path.join(dir, year)
    if not os.path.isdir(path):
        create_dir(dir, year)
        print(year + ' Directory Created')
    else: 
        print('Directory Already Exists')


    for month in months:
        print(year, month)
        path = os.path.join(dir, year, month)
        # print(path)
        if check_file_exists(path + file_type): 
            print('Already Exists')
            continue

        URL = url + '/'+ year +'/'+ month
        # print(URL)
        # get the page by senting request 
        main_page = requests.get(URL)

        if not main_page: 
            print('no '+ year + ' ' + month + ' on website')
            continue
        
        ids = get_ids_from_page(main_page)
        data = []
        big_json = {}
        count = 1
        # print(ids)
        if not ids: 
            df = alternative_scrape(URL, month) 
            if df.empty:
                print('no ids')
                continue
        else: 
            c = len(ids)
            printProgressBar(0, c, prefix = month + ' Progress:', suffix = 'Complete', length = 50)
            for id in ids: 

                printProgressBar(count, c, prefix = month + ' Progress:', suffix = 'Complete', length = 50)
                count += 1
                page = requests.get(forum+id)
                soup = BeautifulSoup(page.content, "lxml")
                script = soup.find("script", id="__NEXT_DATA__")

                # loading the script into json format
                json_object = json.loads(script.string)
            
                data = None 
                if 'forumNote' in json_object['props']['pageProps']: 
                    data=json_object['props']['pageProps']['forumNote']['content']
                big_json[id] = data
            
            df = pd.DataFrame.from_dict(big_json)
            df = modify_df(df)

        path = os.path.join(dir, year, month)
        path += '.csv'
        df.to_csv(path)


    # print('Data have saved in the ' + dir )
    
