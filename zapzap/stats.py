from collections import defaultdict
import pandas as pd
import random
from zapzap.visual import word_cloud, printmd
from zapzap.language import STOP_WORDS

class Stats:
    def __init__(self, df):
        self.df = df
        
    @property
    def PEOPLE(self):
        return list(self.df.name.unique())
    

    def favorite_hours(self):
        df = self.df
        msgs_per_hour = df.groupby(['name', lambda x: df.loc[x].datetime.hour ])

        people_hours = {p: {i:0 for i in range(24)} for p in self.PEOPLE}
        for name_hour, _df in msgs_per_hour:
            name, hour = name_hour
            count = _df.count().datetime
            people_hours[name][hour] = count
        for p in people_hours:
            _df = pd.DataFrame(people_hours[p], index=['count']).transpose()
            _df.plot.bar(legend=False, title=p).set(xlabel="hour of the day", ylabel="messages")


    def characteristic_person(self):
        df = self.df
        text_per_person = df.groupby('name').stext.apply(lambda x: ' '.join(x))
        from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer, TfidfVectorizer
        tfidf = TfidfVectorizer(max_df=0.5)
        tfidf_values = tfidf.fit_transform(text_per_person)
        _df = pd.DataFrame(tfidf_values.toarray(), index=text_per_person.index, columns=sorted(tfidf.vocabulary_))
        random.seed(46)
        shuffled_people = self.PEOPLE
        random.shuffle(shuffled_people)
        for idx, person in enumerate(shuffled_people):
            printmd(f'# Surfista #{person}')
            #printmd(f'# Surfista #{idx}')
            top_words = _df.loc[person].sort_values(ascending=False)[0:20]
            top_words.name = '--'
            print(top_words)
            if top_words[0] == 0: continue # skip people with no words
            word_cloud(top_words.to_dict())
            
            
    def group_most_common_words(self, print_word_count=False ):
        from collections import Counter
        df = self.df

        for m in range(1,12+1): # TODO: change to month/year
            month_text = df[df.datetime.dt.month==(m)].stext.str.cat(sep='\n')
            words = [i for i in month_text.split() if i not in STOP_WORDS() and len(i) > 1]
            if not words: continue
            printmd(f'# **Mes {m}**')
            counter = Counter(words)
            if print_word_count: print(dict(counter.most_common(100)))
            word_cloud(dict(counter.most_common(100)))
