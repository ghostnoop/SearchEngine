from typing import List


def load_index():
    with open('index_sentences.txt', 'r', encoding='utf-8') as f:
        data = f.read().split('\n')
    index = dict()
    all_indexes = set()
    for i in data:
        i, ids = i.split(' ', maxsplit=1)
        ids = set(list(map(int, ids.split(' '))))
        index[i] = ids
        all_indexes = all_indexes | ids
    return index, all_indexes


def load_db():
    with open('sentences.txt', 'r', encoding='utf-8') as f:
        sentences = {idx: i for idx, i in enumerate(f.read().split('\n'))}
    return sentences


class SearchIndexEngine:
    _and = '&'
    _or = '|'
    _not = '~'
    db = load_db()

    def __init__(self):
        self.indexes, self.all_indexes = load_index()
        self.operators = (self._and, self._or, self._not)

    def get_indexes_by_word(self, word: str):
        if word in self.indexes:
            return self.indexes[word]
        return set()

    def search(self, line: str):
        """
                Примеры

                    world & warcraft
                    world | warcraft
                    world & ~warcraft
                    world | ~warcraft

                """
        ids = self.__search(line)
        results = []
        for i in ids:
            results.append(self.db[i])
        return results

    def __search(self, line: str) -> List[str]:

        if line == '':
            return set()

        stack = []
        stack_operators = []

        for word in line.split(' '):
            if word.startswith(self._not):
                word = word[1:]
                current_value = self.get_indexes_by_word(word)
                current_value = self.all_indexes - current_value
                stack.append(current_value)
                continue

            elif word == self._and:
                stack_operators.append(self._and)
                continue
            elif word == self._or:
                stack_operators.append(self._or)
                continue

            stack.append(self.get_indexes_by_word(word))

        result = stack.pop()
        for operator in stack_operators:
            obj2 = stack.pop()

            if operator == self._and:
                result = result & obj2

            elif operator == self._or:
                result = result | obj2
        return result


if __name__ == '__main__':
    sie = SearchIndexEngine()
    answer = sie.search('разнообразный & ~богатый')
    print(answer, len(answer))
