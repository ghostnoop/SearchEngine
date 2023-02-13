import os

import requests

try:
    os.mkdir('downloads')
except:
    pass

with open('urls.csv') as f:
    urls = f.read().strip().split('\n')

counter = 1
index_txt = []

for url in urls:
    response = requests.get(url)
    with open(os.path.join('downloads', f'page{counter}.html'), 'wb') as f:
        f.write(response.content)
    index_txt.append(f'page{counter};{url}')
    print('page', counter)
    counter += 1

with open('index.txt', 'w') as f:
    f.write('\n'.join(index_txt))
