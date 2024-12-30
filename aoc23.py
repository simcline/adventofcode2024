from collections import defaultdict
from itertools import combinations

with open('aoc23.txt') as f:
    l = [x[:-1].split('-') for x in f.readlines()]

#part 1

cnxions = defaultdict(set)

for cn in l:
    cnxions[cn[0]].add(cn[1])
    cnxions[cn[1]].add(cn[0])

res= []
for c1,c2,c3 in combinations(cnxions,3):
    if c2 in cnxions[c1] and c3 in cnxions[c1] and c3 in cnxions[c2] and any(x.startswith('t') for x in (c1,c2,c3)):
        res.append((c1,c2,c3))

len(res)

#part 2
networks = []

for host in cnxions:
    for net in networks:
        if all(host in cnxions[c] for c in net):
            net.add(host)
    networks.append({host})

','.join(sorted(max(networks, key=len)))