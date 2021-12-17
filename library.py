from os.path import exists 
import pandas as pd 
from pandas.core.frame import DataFrame
import os
from datetime import datetime 
from bs4 import BeautifulSoup
import json 
import re 


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
	



