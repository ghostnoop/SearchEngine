import os.path
from pprint import pprint
from typing import List
from numpy import dot
from numpy.linalg import norm

PAGES = 100


def prepare():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'hw4', 'tokens'))
    tokens_index = dict()
    with open('tokens.txt', 'r', encoding='utf-8') as f:
        data = f.read().strip().split('\n')
    for idx, i in enumerate(data):
        tokens_index[i] = idx

    page_tf_idf = dict()
    for page_i in range(1, PAGES + 1):
        name = f'tokens_{page_i}.txt'
        page_vector = []

        with open(os.path.join(path, name), 'r', encoding='utf-8') as f:
            data: List[str] = f.read().strip().split('\n')

        for line in data:
            tf_idf = line.split(' ')[2]
            tf_idf = float(tf_idf)
            page_vector.append(tf_idf)

        page_tf_idf[page_i] = page_vector

    return tokens_index, page_tf_idf


def get_links():
    with open('urls.csv', 'r', encoding='utf-8') as f:
        data = f.read().strip().split('\n')

    links = {}
    for index, i in enumerate(data):
        links[index + 1] = i
    return links


def search(line: str):
    query_vector = [0.0 for _ in tokens_index]
    for word in line.split(' '):
        if word not in tokens_index:
            continue
        index = tokens_index[word]

        query_vector[index] = 1

    results = {}
    for page, v in page_tf_idf.items():
        result = dot(query_vector, v) / (norm(v) * norm(query_vector))
        result = result if str(result) != 'nan' else 0.0
        results[page] = result

    results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
    pages = []

    index = 1
    for k, v in results.items():
        if v == 0.0:
            break

        print(index, links[k], k)
        index += 1


if __name__ == '__main__':
    tokens_index, page_tf_idf = prepare()
    links = get_links()
    # 1 https://habr.com/ru/post/716708/ 1
    search('заболеваний командами')
