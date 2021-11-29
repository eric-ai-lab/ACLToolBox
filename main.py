#!/usr/bin/env python3
import argparse
import pandas as pd 



my_parser = argparse.ArgumentParser(description='Get the related links to the keyword papers')

# ./main.py -month all  -keyword Translation
my_parser.add_argument('-month', metavar='[month or all]', type=str, help='Month searching')
my_parser.add_argument('-keyword', metavar='[keyboard]', nargs='+', type=str, help='keyword', required=True)
args = my_parser.parse_args()


months = ['November', 'October', 'September', 'August', 'July', 'June', 'May']

all = False

keyword = ''
for word in args.keyword: 
	keyword += word + ' '

month = args.month
if month == 'June': 
	month = 'Jun'

index = []



if month in months: 
	path = 'csv/' + month 
elif month == 'all':
	all = True 
else: 
	print('No month is in the database')

print('looking for matching result...')
		
final_df = pd.DataFrame()
if all: 
	for m in months: 
		index = []
		df = pd.read_csv('csv/'+m+'.csv')
		for title in df['title']: 
			try:
				if keyword in title: 
					index.append(df[df['title']==title].index[0])
			except: 
				pass 
		cur = df.iloc[index]
		final_df = final_df.append(cur)
		

else: 
	df = pd.read_csv('csv/' + month + '.csv')
	for title in df['title']: 
		try:
			if keyword in title: 
				index.append(df[df['title']==title].index[0])
		except: 
			pass 
	final_df = df.iloc[index]

final_df['pdf'] = 'https://openreview.net'+final_df['pdf']
final_df['software'] = 'https://openreview.net' + final_df['software']
final_df['data'] = 'https://openreview.net' + final_df['data']

print('saving the result to result.csv')
# print(final_df)
final_df.to_csv('result.csv')
