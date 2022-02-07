from os.path import exists 
import pandas as pd 
from pandas.core.frame import DataFrame
import os
from datetime import datetime 
from bs4 import BeautifulSoup
import json 
import re
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


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


def check_file_exists(filename): 
	"""
	return if file exists in the path
	input: filename (str) 
	output: (bool)
	"""
	if exists(filename): 
		return True 
	return False 

def modify_df(df):
	"""
	return a modified dataframe 
	input: df (dataframe)
	output: df (dataframe)
	"""
	column = df.columns
	df = df.T.reset_index(drop=True)
	df['id'] = column
	cols = list(df.columns)
	cols = [cols[-1]] + cols[:-1]
	df = df[cols]

	return df 

def create_dir(parent_dir, year):
	"""
	creates a directory in the with the path 
	return a path of the directory
	input: parent_dir (str), year (str) 
	output: path (str) 
	"""
	path = os.path.join(parent_dir,year)
	os.mkdir(path)

	return path


def alternative_scrape(url, month): 
    opts = webdriver.ChromeOptions()
    opts.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver = webdriver.Chrome('./chromedriver')
    driver.get(url)
    # time.sleep(3)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source,'lxml')
    header = ['id','title','authorids','authors','TL;DR','abstract','pdf','software','preprint','existing_preprints','preferred_venue','consent','paperhash','reviewer/Editor_reassignment_request','reviewer/Editor_reassignment_justification','data','previous_URL','previous_PDF','response_PDF']
	
    df = pd.DataFrame(columns=header)

    find = soup.find_all("li", {"class": "note"})
    count = len(find)
    if count == 0: 
        return df
    c = 1
    printProgressBar(0, count, prefix = month + ' Progress:', suffix = 'Complete', length = 50)
    for titles in find:
        printProgressBar(c, count, prefix = month + ' Progress:', suffix = 'Complete', length = 50)
        c+=1 
        data = dict()

        id = titles.get('data-id')
        if id is None: 
            continue 

        # print(id)
		
        h4 = titles.find('h4')
        links = h4.find_all('a')

        title = " ".join(links[0].text.split())
        forum = links[0].get('href')
        pdf = links[1].get('href')
		
        data['id'] = id 
        data['title'] = title
        data['forum'] = forum
        data['pdf'] = pdf 
		

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
		
		# print(data)

        df = df.append(data, ignore_index = True)


        print()

	# print(df)
    return df 



def get_ids_from_page(main_page, func=None):
	"""
	get the information needed based on which func to use 
	input: main_page (request), func (year, month, None)
	output: list of ids on the page
	"""
	# beautifulSoup by using lxml to get the raw html and store in soup with different class 
	soup = BeautifulSoup(main_page.content, "lxml")

	# find the script that contains the json data
	script = soup.find("script", id="__NEXT_DATA__")

	# loading the script into json format
	json_object = json.loads(script.string)

	# using regex for parsing the id of each paper

	if func == 'year':
		years = re.findall(r"id=aclweb.org/ACL/ARR/(.+?)\"", str(json_object['props']))
		return years 
	elif func == 'month':
		ids = re.findall(r"\"url\": \"(.+?)\"", str(json_object['props']))
		months = [a.split('/')[-1] for a in ids]
		return months 
	else: 
		ids = re.findall(r"forum\?id=(.+?)\\", str(json_object['props']))
		return ids 
	


