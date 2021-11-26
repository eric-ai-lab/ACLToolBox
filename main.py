#!/usr/bin/env python3
import argparse
from typing import final
import pandas as pd 



my_parser = argparse.ArgumentParser(description='Get the related links to the keyword papers')

# extract keyword=translation pdf=yes data=yes
my_parser.add_argument('-month', metavar='[month or all]', type=str, help='Month searching')
my_parser.add_argument('-keyword', metavar='[keyboard]', type=str, help='keyword', required=True)
my_parser.add_argument('-pdf', metavar='[True, False]', type=bool, help='download the pdf or not')
my_parser.add_argument('-data', metavar='[True, False]', type=bool, help='download the data or not')

args = my_parser.parse_args()


months = ['November', 'October', 'September', 'August', 'July', 'June', 'May']

all = False

keyword = args.keyword 
month = args.month
pdf = args.pdf
data = args.data

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
					# print(title)
					index.append(df[df['title']==title].index[0])
					# index = df[df['title']==title].index[0]
					# print(index)
					# id = df.iloc[[index]]
					# print(id)
					# if pdf: 
					# 	pdf_link = 'https://openreview.net' + df['pdf'].iloc[index]
					# 	print(pdf_link)
					# if data: 
			except: 
				pass 
		cur = df.iloc[index]
		final_df = final_df.append(cur)
		

else: 
	df = pd.read_csv('csv/' + month + '.csv')
	for title in df['title']: 
		try:
			if keyword in title: 
				# print(title)
				index.append(df[df['title']==title].index[0])
				# index = df[df['title']==title].index[0]
				# print(index)
				# id = df.iloc[[index]]
				# print(id)
				# if pdf: 
				# 	pdf_link = 'https://openreview.net' + df['pdf'].iloc[index]
				# 	print(pdf_link)
				# if data: 
		except: 
			pass 
	final_df = df.iloc[index]


print('saving the result to result.csv')
# print(final_df)
final_df.to_csv('result.csv')
