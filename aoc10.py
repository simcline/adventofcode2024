from itertools import product

with open('aoc10.txt') as f:
    l = [list(map(int,x[:-1])) for x in f.readlines()]

starts = [(i,j) for i,j in product(range(len(l)), range(len(l[0]))) if l[i][j] == 0 ]

#part 1

def explore_from(start):

    explored = {start}

    keepgoing = True
    while keepgoing:
        nexplored = len(explored)
        adjacents = set()
        for x in explored:
            adjacents |= set(
                filter(lambda y: 0 <= y[0] < len(l) and 0 <= y[1] < len(l[0]) and l[y[0]][y[1]] == l[x[0]][x[1]] + 1,
                       map(lambda y: (x[0]+y[0], x[1]+y[1]), ((0,1), (1,0), (-1,0), (0,-1)))))
        explored |= adjacents
        keepgoing = len(explored) > nexplored

    return sum(map(lambda x: l[x[0]][x[1]] == 9, explored))

sum(map(explore_from, starts))

#part 2

def counttrails_from(start):
    paths = [[start]]
    finished_paths = []

    while len(paths):
        to_remove = []
        to_add = []
        for p in paths:
            x = p[-1]
            if l[x[0]][x[1]] == 9:
                finished_paths.append(p)
                to_remove.append(p)
            else:
                nm = tuple(
                filter(lambda y: 0 <= y[0] < len(l) and 0 <= y[1] < len(l[0]) and l[y[0]][y[1]] == l[x[0]][x[1]] + 1,
                       map(lambda y: (x[0]+y[0], x[1]+y[1]), ((0,1), (1,0), (-1,0), (0,-1)))))
                match len(nm):
                    case 0:
                        to_remove.append(p)
                    case 1:
                        p.append(nm[0])
                    case x if x > 1:
                        to_remove.append(p)
                        to_add.extend([p + [q] for q in nm])
        for r in to_remove:
            paths.remove(r)
        paths.extend(to_add)

    return len(finished_paths)

sum(map(counttrails_from, starts))