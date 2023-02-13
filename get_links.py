import requests
from bs4 import BeautifulSoup

url = 'https://habr.com/ru/all/page{}/'
base_url = 'https://habr.com'
links = []
counter = 0
while len(links) < 100:

    resp = requests.get(url.format(counter + 1))
    # tm-article-snippet__title
    soup = BeautifulSoup(resp.content, "html.parser")

    for title in soup.find_all('h2', {"class": "tm-article-snippet__title"}):
        print(title.find('a').get('href'))
        link = title.find('a').get('href')
        links.append(f'{base_url}{link}')

    counter += 1

with open('urls.csv', 'w') as f:
    f.write('\n'.join(links))
