from itertools import pairwise

with open('aoc5.txt') as f:
    orderings = []
    queries = []
    for line in f.readlines():
        if '|' in line:
            orderings.append(line[:-1])
        elif ',' in line:
            queries.append(list(map(int,line[:-1].split(','))))

#part 1

class Page:
    def __init__(self, pagenum):
        self.pagenum = pagenum

    def __lt__(self, other):
        return f'{self.pagenum}|{other.pagenum}' in orderings

queries = list(map(lambda x: list(map(Page, x)), queries))

def evaluate_query(query):
    for q1, q2 in pairwise(query):
        if not (q1 < q2):
            return 0
    return query[len(query)//2].pagenum

sum(map(evaluate_query, queries))

#part 2

sum(map(evaluate_query, map(sorted, filter(lambda x: not evaluate_query(x), queries))))
