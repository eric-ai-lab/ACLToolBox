import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
# from nltk.stem.regexp import RegexpStemmer
# from nltk.stem.lancaster import LancasterStemmer
from os.path import exists 
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from pattern.text.en import singularize


nltk.download('punkt')
nltk.download("averaged_perceptron_tagger")
# stemmer = RegexpStemmer('s$|ies$')
# st = LancasterStemmer()

def check_file_exists(filename): 
  if not exists(filename): 
    return True 
  return False 

def add_to_dict(phrase, freq):
  if phrase in freq: 
      freq[phrase] += 1
  else: 
    freq[phrase] = 1 

def parse_words(title): 
  try:
    title = title.lower() 
    title_words = word_tokenize(str(title))
    return title_words
  except:
    return None 

def parse_nouns_to_frequency(title, freq):
  # print(title)
  title_words = parse_words(title)
  if not title_words: 
    return 
  # print(title_words)
  words = [singularize(plural) for plural in title_words]
  # print(words)
  title_tags = nltk.pos_tag(words)
  grammar = "NP: {<JJ>*<NN>?<NN>?<NN>?}"
  chunk_parser = nltk.RegexpParser(grammar)
  tree = chunk_parser.parse(title_tags)
  for subtree in tree.subtrees(lambda t: t.label() == 'NP'):
    # print(subtree.leaves())
    phrase = ""
    for i in subtree.leaves(): 
      phrase += i[0] + ' ' 
    add_to_dict(phrase, freq)





def parse_verbs_to_frequency(title, freq):
  title_words = parse_words(title)
  if not title_words:
    return 
  title_tags = nltk.pos_tag(title_words)
  grammar_v = "V: {<VB>|<VBD>|<VBG>|<VBZ>}"
  chunk_parser_verb = nltk.RegexpParser(grammar_v)
  tree_v = chunk_parser_verb.parse(title_tags)
  for subtree in tree_v.subtrees(lambda t: t.label() == 'V'):
    # print(subtree.leaves())
    phrase = ""
    for i in subtree.leaves(): 
      phrase += i[0] + ' ' 
    add_to_dict(phrase, freq)


def graph_wordcloud(freq, name):
	# df = df.rename(columns={'Unnamed: 0': 'phrase', 1: 'frequency'})
	# freq = dict(zip(df['phrase'], df['frequency']))

  for key in freq.keys():
    if key in STOPWORDS:
      del freq[key]
  
  wordcloud = WordCloud(width = 800, height = 800, background_color ='white', min_font_size = 10).generate_from_frequencies(freq)

  plt.figure(figsize = (8, 8), facecolor = None)
  plt.imshow(wordcloud) 
  plt.axis("off")
  plt.tight_layout(pad = 0)

  # if want to save the pic as png
  plt.savefig(name + '.png') 
  plt.show()	



def main(): 
  dir = "csv/"
  months = {1:'January', 2:'Feburary', 3:'March', 4:'April', 5:'May', 6:'Jun', 7:'July',8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
  years = {2021:'2021', 2022:'2022'}
  freq = {} 

  for year in years.values():
    for month in months.values(): 
        file_name = dir + year + ' ' +month + '.csv'
        if check_file_exists(file_name):
          # print('No month is in the database')
          continue
        df = pd.read_csv(file_name)
        
        # iterate through the csv file
        for title in df['title']:
            parse_nouns_to_frequency(title, freq)
            # parse_verbs_to_frequency(title, freq)
          
  # print(freq)
  df = pd.DataFrame(data=freq.values(), index=freq.keys(),columns = ['frequency'])
  column = df.index
  df = df.reset_index(drop=True)
  df['phrase'] = column 
  cols = list(df.columns)
  cols = [cols[-1]] + cols[:-1]
  df = df[cols]
  df = df.sort_values(by=['frequency'], ascending=False, ignore_index=True)
  # print(df)
  # df.to_csv("title_verb_freq.csv")

  graph_wordcloud(freq, 'title')





if __name__ == '__main__':
  main()