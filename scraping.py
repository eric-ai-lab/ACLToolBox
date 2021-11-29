#!/usr/bin/env python
from pandas.core.frame import DataFrame
import requests 
from bs4 import BeautifulSoup
import json
import re
import pandas as pd 


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()



dir = 'csv/'
# June is written as Jun on website 
months = ['November', 'October', 'September', 'August', 'July', 'Jun', 'May']



url = "https://openreview.net/group?id=aclweb.org/ACL/ARR/2021/" 
forum = 'https://openreview.net/forum?id='
pdf = 'https://openreview.net/pdf?id=' 

print('Starting scraping the data...')
printProgressBar(0, len(months), prefix = 'Progress:', suffix = 'Complete', length = 50)
count = 0 
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
        printProgressBar(count + 1, len(ids), prefix = month + ' Progress:', suffix = 'Complete', length = 50)
        count += 1
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
  
