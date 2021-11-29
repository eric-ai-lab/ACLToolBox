import pandas as pd 


df = pd.read_csv('../csv/abstract_freq.csv')
df.sort_values(by=['frequency'], ascending=False, ignore_index=True, inplace=True) 

df.to_csv('abstract_freq_desc.csv')

