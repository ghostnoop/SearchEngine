import requests

with open('urls.csv','r',encoding='utf-8') as f:
    data=f.read().strip().split('\n')

titles=[]
for i in data:
    resp = requests.get(i)

    al = resp.text
    title = al[al.find('<title>') + 7: al.find('</title>')]
    title=str(title)
    titles.append(title)

with open('titles.csv','w',encoding='utf-8') as f:
    f.write('\n'.join(titles))


