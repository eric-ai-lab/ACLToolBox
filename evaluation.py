# from geeksforgeeks 

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd

dir = "csv/"

months = ['November', 'October', 'September', 'August', 'July', 'Jun', 'May']

for month in months: 
    df = pd.read_csv(dir + month + ".csv")
    
    comment_words = ''
    stopwords = set(STOPWORDS)
    
    # iterate through the csv file
    # for val in df['title']:
    for val in df['abstract']:
        
        # typecaste each val to string
        val = str(val)
    
        # split the value
        tokens = val.split()

        tokens = [x for x in tokens if x != 'nan']
        
        # Converts each token into lowercase
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        
        comment_words += " ".join(tokens)+" "
    

    wordcloud = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    stopwords = stopwords,
                    min_font_size = 10).generate(comment_words)
    
    # plot the WordCloud image                      
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    
    # plt.savefig(month+'_title.png')
    # plt.savefig(month+'_abstract.png')
    plt.show()
  