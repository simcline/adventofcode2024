from collections import defaultdict
from itertools import product

import numpy as np

with open('aoc16.txt') as f:
    l = [x[:-1] for x in f.readlines()]

start = [(i,j) for i,j in product(range(len(l)), range(len(l[0]))) if l[i][j] == 'S'][0]
target = [(i,j) for i,j in product(range(len(l)), range(len(l[0]))) if l[i][j] == 'E'][0]

distances = defaultdict(lambda : np.Inf)
boundary_unvisited = {(*start, (0,1)):0}  #x,y,lastdirection
distances[(*start, (0,1))]=0
visited = set()

def get_neighbours(x):
    return set(filter(lambda y:l[y[0]][y[1]] in ('.', 'E', 'S'),  map(lambda y: (x[0]+y[0], x[1]+y[1], y), ((0,1), (1,0), (0,-1), (-1,0)))))

while len(boundary_unvisited):
    nextstep, d = min(boundary_unvisited.items(), key = lambda x: x[1])
    lastdir = nextstep[2]
    if nextstep in boundary_unvisited: del boundary_unvisited[nextstep]
    nnext = get_neighbours(nextstep)

    for x in nnext:
        nextdir = x[2]
        if lastdir is None or lastdir == nextdir:
            delta_dist = 1
        else:
            delta_dist = 1001

        if d + delta_dist < distances[x]:
            distances[x] = d + delta_dist
        if x not in visited:
            boundary_unvisited[x] = distances[x]

    visited.add(nextstep)


d0=min(distances[(*target,y)] for y in ((0,1), (1,0), (0,-1), (-1,0)))
d0
# part 2

paths = [[(*start, (0,1))]]
validpaths = []

while True:
    newpaths = []
    for p in paths:
        nextpaths = [p+[q] for q in filter(lambda x: ((distances[p[-1]] + 1 == distances[x]) or (distances[p[-1]] + 1001 == distances[x])) and distances[x] <= d0, get_neighbours(p[-1]))]
        newpaths.extend(nextpaths)

    validpaths.extend(filter(lambda x:(x[-1][0],x[-1][1]) == target, newpaths))
    paths=newpaths
    if not len(newpaths):
        break

len(set(x for t in map(lambda x: [(y[0], y[1]) for y in x],validpaths) for x in t))