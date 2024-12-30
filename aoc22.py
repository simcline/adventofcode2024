from collections import defaultdict
import numpy as np

with open('aoc22.txt') as f:
    l = [int(x[:-1]) for x in f.readlines()]

def get_next(x, n):
    if n == 0:
        return x
    x = ((x * 64) ^ x) % 16777216
    x = ((x // 32) ^ x) % 16777216
    return get_next(((x * 2048) ^ x) % 16777216, n - 1)

#part 1
sum(map(lambda x: get_next(x, 2000), l))

#part 2
def get_all(x, n, ret=None):
    ret = [x] if ret is None else ret
    if n == 0:
        return ret
    x = ((x * 64) ^ x) % 16777216
    x = ((x // 32) ^ x) % 16777216
    x = ((x * 2048) ^ x) % 16777216
    ret.append(x)
    return get_all(x, n - 1, ret)


prices = [list(map(lambda x: x % 10, get_all(x, 2000))) for x in l]
delta = list(map(np.diff, prices))
deltas = [[] for _ in range(len(l))]

for j, d in enumerate(delta):
    for i in range(len(delta[0]) - 3):
        deltas[j].append(tuple(d[i:i + 4]))

evals = defaultdict(lambda: 0)
is_out = defaultdict(set)

for i in range(len(deltas[0])):
    for j in range(len(deltas)):
        seq = deltas[j][i]
        if j not in is_out[seq]:
            evals[seq] += prices[j][i + 4]
            is_out[seq].add(j)

best = max(evals, key=evals.get)
evals[best]
