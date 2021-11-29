import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download("averaged_perceptron_tagger")

dir = "../csv/"

months = ['November', 'October', 'September', 'August', 'July', 'Jun', 'May']

freq = {} 
# months = ['Jun']
for month in months: 
    df = pd.read_csv(dir + month + ".csv")
    
    # iterate through the csv file
    for title in df['abstract']:
        try:
          # print(title)
          title = title.lower()
          title_words = word_tokenize(str(title))
          title_tags = nltk.pos_tag(title_words)
          grammar = "NP: {<JJ>*<NN>?<NN>?<NN>}"
          chunk_parser = nltk.RegexpParser(grammar)
          tree = chunk_parser.parse(title_tags)
        #   print(tree)
          for subtree in tree.subtrees(lambda t: t.label() == 'NP'):
            # print(subtree.leaves())
            phrase = ""
            for i in subtree.leaves(): 
              phrase = phrase + i[0] + ' ' 

            if phrase in freq: 
              freq[phrase] += 1
            else: 
              freq[phrase] = 1 
            # print(phrase)
            # print(freq)
        except:
          pass
        
    # print(freq)
    df = pd.DataFrame(data=freq.values(), index=freq.keys(),columns = ['frequency'])
    df = df.sort_index()
    # print(df)
    df.to_csv("abstract_freq.csv")