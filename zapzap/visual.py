from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import random

def word_cloud(dict_word_size):
    random.seed(46)
    from wordcloud import WordCloud
    dict_word_size = {k:5+v for k,v in dict_word_size.items() if v}
    wc = WordCloud(stopwords=[], color_func=lambda *_, **a: random.choice(['white','yellow','grey']), relative_scaling=1
                  , max_font_size=100, width=600, height=500, random_state=42 ).generate_from_frequencies(dict_word_size)
    plt.figure(figsize=(12, 10))
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    
    
from IPython.display import Markdown, display
def printmd(s):
    display(Markdown(s)) 

from IPython.display import display, HTML
def display_nl(dataframe):
    return HTML(dataframe.to_html().replace("\\n","<br>") )