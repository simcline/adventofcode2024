from collections import defaultdict
from itertools import product
import numpy as np

with open('aoc20.txt') as f:
    l = f.readlines()

w = list(map(lambda x: [y for y in x if y != '\n'], l))

start = [(i, j) for i, j in product(range(len(w)), range(len(w[0]))) if w[i][j] == 'S'][0]
target = [(i, j) for i, j in product(range(len(w)), range(len(w[0]))) if w[i][j] == 'E'][0]

w[start[0]][start[1]] = '.'
w[target[0]][target[1]] = '.'

nrows, ncols = len(w), len(w[0])


def get_neighbours(x, cheatpoint=None):
    return set(filter(lambda y: w[y[0]][y[1]] == '.' or y == cheatpoint,
                      filter(lambda y: 0 <= y[0] < nrows and 0 <= y[1] < ncols,
                             map(lambda y: (x[0] + y[0], x[1] + y[1]), ((0, 1), (1, 0), (-1, 0), (0, -1))))))


def get_distances(start=start):
    distances = defaultdict(lambda: np.Inf)
    boundary_unvisited = {start: 0}
    distances[start] = 0
    visited = set()

    while len(boundary_unvisited):
        nextstep, d = min(boundary_unvisited.items(), key=lambda x: x[1])
        if nextstep in boundary_unvisited: del boundary_unvisited[nextstep]
        nnext = get_neighbours(nextstep)

        for x in nnext:
            delta_dist = 1

            if d + delta_dist < distances[x]:
                distances[x] = d + delta_dist
            if x not in visited:
                boundary_unvisited[x] = distances[x]

            visited.add(x)

    return distances


distances = get_distances()
initdist = distances[target]

def l1dist(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])

def get_number_cheats_larger_than(k, maxcheats):
    cheats={}

    def cheat_from(x):
        possible_cheat_endpoint = filter(
            lambda y: 0 <= y[0] < nrows and
                      0 <= y[1] < ncols and
                      2 <= l1dist(x, y) <= maxcheats and
                      w[y[0]][y[1]] == '.',
            ((x[0] + i, x[1] + j) for i, j in product(range(-maxcheats, maxcheats + 1), repeat=2))
        )

        for p in possible_cheat_endpoint:
            dist_to_p = l1dist(x, p)
            newdist = distances[x] + dist_to_p + initdist - distances[p]
            if newdist < initdist:
                cheats[(x, p)] = newdist

    for x in product(range(nrows), range(ncols)):
        if w[x[0]][x[1]] == '.':
            cheat_from(x)


    return sum(initdist - x >= k for x in cheats.values())

#part 1
get_number_cheats_larger_than(100,2)

#part 2
get_number_cheats_larger_than(100,20)