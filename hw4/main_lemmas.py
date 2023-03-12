import math
import os
from collections import defaultdict

from bs4 import BeautifulSoup
import spacy
import nltk
from nltk.corpus import stopwords

nlp = spacy.load("ru_core_news_sm")

russian_stopwords = stopwords.words("russian")


def extract(text: str):
    doc = nlp(text.strip())
    # print([(w.text, w.pos_) for w in doc])
    texts = []
    for i in doc:
        if i.text in ('\n','',' '):
            continue
        if i.is_alpha and not i.like_num and not i.is_punct and i.text.lower() not in russian_stopwords:
            texts.append(i.text)
    return ' '.join(texts)

def get_all_words_from_downloads():
    words_all = []
    words_by_page = defaultdict(set)

    for i in range(1, 101):
        with open(os.path.join('..', 'downloads', f'page{i}.html'), 'rb') as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            data = extract(soup.get_text(" ").lower())
            data = data.split(' ')
            words_all.extend(data)
            words_by_page[i] = set(data)

    return words_all, words_by_page


def counter(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = f.read().strip().split('\n')

    words = []

    for i in data:
        word = i.split(' ')
        words.append(word)

    words_all, words_by_page = get_all_words_from_downloads()

    # {"word":{"tf":0,"idf":0}}
    word_tf_idf = {}
    for word in words:
        counter = 0
        for i in words_all:
            if i in word:
                counter += 1
        counter_page = 0
        for i, v in words_by_page.items():
            for word_i in word:
                if word_i in v:
                    counter_page += 1

        tf = counter / len(words_all)
        idf = (len(words_by_page) / counter_page if counter_page > 0 else 0.0)
        idf = math.log(idf) if idf > 0 else 0.0
        tf_idf = tf * idf

        # tf = round(tf, 2)
        # tf_idf = round(tf_idf, 2)

        word_tf_idf[word[0]] = dict(tf=tf, tf_idf=tf_idf)

    return word_tf_idf


def writer(file_name, word_tf_idf):
    #     <термин><пробел><idf><пробел><tf-idf><\n>
    with open(f'hw_{file_name}', 'w', encoding='utf-8') as f:
        s = []
        for i, v in word_tf_idf.items():
            s.append(f'{i} {v["tf"]} {v["tf_idf"]}\n')
        f.write(''.join(s))


if __name__ == '__main__':
    for i in ['lemmas.txt']:
        count = counter(i)
        writer(i, count)
