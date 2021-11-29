# from word import STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS


# Reads 'Youtube04-Eminem.csv' file
df = pd.read_csv('title_freq.csv')
df = df.rename(columns={'Unnamed: 0': 'phrase', 1: 'frequency'})
print(df)
freq = dict(zip(df['phrase'],df['frequency']))
print(freq)


stopwords = set(STOPWORDS)
stopwords.add('s')
stopwords.add('language')
stopwords.add('use')
stopwords.add('based')
stopwords.add('model')
stopwords.add('word')
stopwords.add('impact')
stopwords.add('case')
stopwords.add('impact')
stopwords.add('study')
stopwords.add('causal')
stopwords.add('graph')


wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate_from_frequencies(freq)



# plot the WordCloud image                      
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)

plt.savefig('title.png') 
plt.show()
