import os
from collections import defaultdict
from bs4 import BeautifulSoup

import spacy
import nltk
from nltk.corpus import stopwords
import glob

# spacy.cli.download("ru_core_news_sm")
# nltk.download("stopwords")

nlp = spacy.load("ru_core_news_sm")

russian_stopwords = stopwords.words("russian")

lemmas_dct = defaultdict(set)
tokens = set()


def extract(text: str):
    doc = nlp(text.strip())
    # print([(w.text, w.pos_) for w in doc])
    for i in doc:
        if i.text in ('\n','',' '):
            continue
        if i.is_alpha and not i.like_num and not i.is_punct and i.text.lower() not in russian_stopwords:
            tokens.add(i.text)
            lemmas_dct[i.lemma_].add(i.text)


files = glob.glob(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'downloads','*.*')))
counter=0
for file in files:
    with open(file,'rb') as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        extract(soup.text.lower())
    print(counter)
    counter+=1

print(tokens)
print(lemmas_dct)

with open('tokens.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(list(tokens)))

lemmas_lst=[]
for key,values in lemmas_dct.items():
    line = f'{key} '+' '.join(list(values))
    lemmas_lst.append(line)

with open('lemmas.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(lemmas_lst))

# print(files)