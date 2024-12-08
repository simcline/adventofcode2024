from collections import defaultdict
from itertools import combinations

with open('aoc8.txt') as f:
    l = [x[:-1] for x in f.readlines()]

nodes = defaultdict(list)

for i,line in enumerate(l):
    for j,c in enumerate(line):
        if c!='.':
            nodes[c].append((i,j))

#part 1

antinodes = set()

for nds in nodes.values():
    for n, m in combinations(nds, 2):
        candidates = ((2*m[0]-n[0], 2*m[1]-n[1]), (2*n[0]-m[0], 2*n[1]-m[1]))
        for c in candidates:
            if not (c[0]<0 or c[0]>=len(l[0]) or c[1]<0 or c[1]>=len(l)):
                antinodes.add(c)

len(antinodes)

# part 2

antinodes = set()

for nds in nodes.values():
    for n, m in combinations(nds, 2):
        k=0
        while True:
            c = (n[0]+ k*(m[0]-n[0]), n[1]+k*(m[1]-n[1]))
            if not (c[0] < 0 or c[0] >= len(l[0]) or c[1] < 0 or c[1] >= len(l)):
                antinodes.add(c)
                k+=1
            else:
                break
        k=-1
        while True:
            c = (n[0] + k * (m[0] - n[0]), n[1] + k * (m[1] - n[1]))
            if not (c[0] < 0 or c[0] >= len(l[0]) or c[1] < 0 or c[1] >= len(l)):
                antinodes.add(c)
                k -= 1
            else:
                break

len(antinodes)