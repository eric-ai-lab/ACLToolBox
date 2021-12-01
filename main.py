#!/usr/bin/env python3
import argparse
import pandas as pd 
from os.path import exists 

months = {1:'January', 2:'Feburary', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July',8:'Auguest', 9:'September', 10:'October', 11:'November', 12:'December'}
years = {2021:'2021', 2022:'2022'}

def query(all, keyword, month, year, csv):

	index = [] 
	final_df = pd.DataFrame()
	if all: 
		for y in years.values():
			for m in months.values(): 
				file_name = 'csv/' +y +' '+m + '.csv'
				if not exists(file_name):
					# print('No month is in the database')
					continue
				index = []
				df = pd.read_csv(file_name)
				for title in df['title']: 
					try:
						if keyword in title: 
							index.append(df[df['title']==title].index[0])
					except: 
						pass 
				cur = df.iloc[index]
				final_df = final_df.append(cur)
			

	else: 
		df = pd.read_csv('csv/' + year+' '+month + '.csv')
		for title in df['title']: 
			try:
				if keyword in title: 
					index.append(df[df['title']==title].index[0])
			except: 
				pass 
		final_df = final_df.append(df.iloc[index])


	final_df['pdf'] = 'https://openreview.net'+final_df['pdf']
	final_df['software'] = 'https://openreview.net' + final_df['software']
	final_df['data'] = 'https://openreview.net' + final_df['data']
	final_df['forum'] = 'https://openreview.net/forum?id=' + final_df['id']


	print(final_df[['title', 'forum']].to_string())

	if csv=='Y':
		final_df.to_csv('result.csv')
		print('saving the result to result.csv')



my_parser = argparse.ArgumentParser(description='Get the related links to the keyword papers')

# ./main.py -year 2021 -month None -keyword Translation
my_parser.add_argument('-year', metavar='(2021-2022) | none = all', type=int, help='Year searching', default=2021)
my_parser.add_argument('-month', metavar='(1-12) | none = all', type=int, help='Month searching', default = None)
my_parser.add_argument('-keyword', metavar='keyword', nargs='+', type=str, help='keyword', required=True)
my_parser.add_argument('-csv', metavar='y or n', type=str, help='save csv')
args = my_parser.parse_args()


all = True
# parse the keyword arg
keyword = ''
if not args.keyword: 
	print("You didn't input keyword!")

for word in args.keyword: 
	keyword += word.capitalize() + ' '

# parse the year arg 
year = args.year

# parse the month arg
month = ''
if args.month == None:
	all = True
else: 
	all = False
	month = months[args.month]

# parse the csv arg
csv = None 
if args.csv:
	csv = args.csv.capitalize()
else: 
	csv = None

print('looking for matching result...')
query(all, keyword, month, year, csv)