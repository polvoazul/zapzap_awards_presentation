from collections import defaultdict, Counter
import pandas as pd
import random
from zapzap.visual import word_cloud, printmd, display_nl
from zapzap.language import STOP_WORDS
import logging

from IPython.display import display, HTML

display_chat = display

class Awards:
    def __init__(self, df, group_name):
        self.df = df
        self.group_name = group_name
        
    def metalinguistic(self):
        group_name = self.group_name.lower() # sanitize text
        regexp = '|'.join(w for w in group_name.split() if w not in STOP_WORDS())
        logging.root.info(regexp)
        _df = self.df[self.df.stext.str.contains(regexp)][['short_links_text', 'name', 'datetime']]
        pd.set_option('display.max_colwidth', -1)
        #pd.set_option('display.max_rows', -1)
        display(display_nl(_df))
        top = _df.groupby('name').count().datetime.sort_values(ascending=False)
        print(top)
        
    def early_riser(self):
        msgs_per_day = self.df.groupby([lambda x: self.df.loc[x].datetime.date()])
        first_post_of_day = []
        for day, _df in msgs_per_day:
            early = _df.loc[(_df.datetime.dt.hour > 6) & (_df.datetime.dt.hour < 10)]
            if not early.empty: first_post_of_day.append(early.sort_values(by='datetime').iloc[0].tolist())
        first_post_of_day = pd.DataFrame(first_post_of_day, columns=early.columns)[['short_links_text', 'name', 'datetime']]
        display(first_post_of_day)
        print(first_post_of_day.groupby('name').count().datetime.sort_values(ascending=False))
        
    def shouts(self):
        df  = self.df
        import string
        import numpy as np
        text_per_name = df.groupby(['name']).text.apply(lambda x: ''.join(x)).to_dict()
        letters_per_name = {n: Counter(t) for n, t in text_per_name.items()}
        def get_small_big_ratio(counter):
            small, big = 0, 0
            acentos = 'áâãàçéêíóôõú'
            for l in string.ascii_lowercase + acentos: small += counter.get(l, 0)
            for l in string.ascii_uppercase + acentos.upper(): big += counter.get(l, 0)
            return 100*big/(small+big) if small + big else float('nan')
        scores = { n: get_small_big_ratio(counter) for n, counter in letters_per_name.items()}
        scores = sorted(scores.items(), key=lambda x: x[1])
        gritos = df.loc[np.logical_and(
            df.short_links_text.apply(lambda t:get_small_big_ratio(Counter(t))) > 51, df.text.str.len() > 5)
        ].copy()
        grito_ratio = gritos.groupby('name').count().datetime/df.groupby('name').count().datetime * 100

        gritos['order'] = gritos.name.apply(lambda n: grito_ratio[n] if not pd.isna(n) else float('inf'))
        #display_nl(sort_values(by='name'))
        display_chat(display_nl(gritos.sort_values(['order', 'datetime'])['text name datetime'.split()]))
        printmd('## Medido em gritos a cada 100 mensagens. \n ### Um grito eh qq mensagem com mais letras UPPERCASE do que lowercase. ')
        print(grito_ratio.sort_values(ascending=False))
        #TODO: trocar pra gritos / 100 mensagens