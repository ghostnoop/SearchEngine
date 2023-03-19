import string
from collections import defaultdict

with open('lemmas.txt', 'r', encoding='utf-8') as f:
    sentences = f.read().strip().split('\n')

index = defaultdict(list)


def clear_sentence(line: str):
    new_line = []
    for i in line.lower().strip().split(' '):
        if len(i) <= 2:
            continue
        new_line.append(i)
    line = ' '.join(new_line)

    to_clear_signs = tuple(string.digits + string.punctuation)
    new_line = []
    for i in line:
        if i not in to_clear_signs:
            new_line.append(i)
    new_line = ''.join(new_line)
    return new_line


for idx, sentence in enumerate(sentences):
    words = clear_sentence(sentence).split(' ')
    for word in words:
        if len(word) <= 2:
            continue
        index[word].append(idx)

text = [f'{k} ' + ' '.join(map(str, list(v))) for k, v in index.items()]

with open('index_sentences.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(text))
