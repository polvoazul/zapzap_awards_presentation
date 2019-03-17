import requests
from functools import lru_cache

@lru_cache(10)
def STOP_WORDS():
    return (
            requests.get('https://raw.githubusercontent.com/stopwords-iso/stopwords-pt/master/stopwords-pt.json').json()
            + 'q pra hahaha to tá vc cara eh ta acho vou pq tô pro ja la'.split()
    )
