from collections import defaultdict
import numpy as np

with open('aoc18.txt') as f:
    l = list(map(lambda x: tuple(map(int,x.split(','))), [x[:-1] for x in f.readlines()]))

n = 71

def get_distance(n_bytes):
    w = [['.']*n for _ in range(n)]
    for p in l[:n_bytes]:
        w[p[0]][p[1]] = '#'

    start = (0,0)
    target = (n-1,n-1)

    distances = defaultdict(lambda : np.Inf)
    boundary_unvisited = {start:0}
    distances[start]=0
    visited = set()

    def get_neighbours(x):
        return set(filter(lambda y:w[y[0]][y[1]] == '.',  filter(lambda y: 0<=y[0]<n and 0<=y[1]<n, map(lambda y: (x[0]+y[0], x[1]+y[1]), ((0,1), (1,0), (0,-1), (-1,0))))))

    while len(boundary_unvisited):
        nextstep, d = min(boundary_unvisited.items(), key = lambda x: x[1])
        if nextstep in boundary_unvisited: del boundary_unvisited[nextstep]
        nnext = get_neighbours(nextstep)

        for x in nnext:
            delta_dist = 1

            if d + delta_dist < distances[x]:
                distances[x] = d + delta_dist
            if x not in visited:
                boundary_unvisited[x] = distances[x]

        visited.add(nextstep)

    return distances[target]

#part 1

get_distance(1024)

#part 2

for n_byte in range(1024, len(l)):
    if get_distance(n_byte) == np.Inf:
        print(l[n_byte-1])
        break
