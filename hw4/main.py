import math
import os
from collections import defaultdict, Counter

from bs4 import BeautifulSoup
import spacy
import nltk
from nltk.corpus import stopwords

nlp = spacy.load("ru_core_news_sm")

russian_stopwords = stopwords.words("russian")
PAGES = 101


def extract(text: str):
    doc = nlp(text.strip())
    # print([(w.text, w.pos_) for w in doc])
    texts = []
    for i in doc:
        if i.text in ('\n', '', ' '):
            continue
        if i.is_alpha and not i.like_num and not i.is_punct and i.text.lower() not in russian_stopwords:
            texts.append(i.text)
    return ' '.join(texts)


def get_all_words_from_downloads():
    words_by_page = defaultdict(set)

    for i in range(1, PAGES):
        with open(os.path.join('..', 'downloads', f'page{i}.html'), 'rb') as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            data = extract(soup.get_text(" ").lower())
            data = data.split(' ')
            words_by_page[i] = (set(data), Counter(data), len(data))

    return words_by_page


def counter(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = f.read().strip().split('\n')

    words = []

    words_by_page = get_all_words_from_downloads()

    for i in data:
        word = i.split(' ', maxsplit=1)[0]
        words.append(word)

    for page_i in range(1, PAGES):
        word_tf_idf = {}
        _, words_counter, size = words_by_page[page_i]
        for word in words:
            tf = words_counter.get(word, 0) / size

            count_by_page = 0
            for j in words_by_page.values():
                if word in j[0]:
                    count_by_page += 1

            idf = math.log(len(words_by_page) / max(count_by_page, 1))

            tf_idf = tf * idf

            word_tf_idf[word] = dict(tf=tf, tf_idf=tf_idf)

        file_name_without_suffix = file_name.replace('.txt', '')
        writer(f'{file_name_without_suffix}/tokens_{page_i}.txt', word_tf_idf)
        print('page', page_i, 'size', PAGES)



def writer(file_name, word_tf_idf):
    #     <термин><пробел><idf><пробел><tf-idf><\n>
    with open(file_name, 'w', encoding='utf-8') as f:
        s = []
        for i, v in word_tf_idf.items():
            s.append(f'{i} {v["tf"]} {v["tf_idf"]}\n')
        f.write(''.join(s))


if __name__ == '__main__':
    for i in ['tokens.txt','lemmas.txt']:
        count = counter(i)
        writer(i, count)
