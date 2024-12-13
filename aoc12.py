from itertools import product

with open('aoc12.txt') as f:
    l = [x[:-1] for x in f.readlines()]

def get_neighbours(c):
    return set(( min(max(c[0]+i,0), len(l)-1),  min(max(c[1]+j,0), len(l[0])-1)) for i,j in ((-1,0),(1,0),(0,1),(0,-1))) - {c}

def connected_component(g):
    cc = set()
    frontier = {g}
    perimeter = 0
    while len(frontier):
        to_add = set()
        to_remove = set()
        for c in frontier:
            neihbours = get_neighbours(c)
            perimeter += sum(map(lambda x:l[x[0]][x[1]] != l[c[0]][c[1]], neihbours)) + max(4-len(neihbours),0)
            for neighb in neihbours:
                if neighb not in frontier and neighb not in cc and l[c[0]][c[1]] == l[neighb[0]][neighb[1]]:
                    to_add.add(neighb)
            to_remove.add(c)
            cc.add(c)
        frontier -= to_remove
        frontier |= to_add
    return cc, perimeter

explored = set()
price = 0
for x in product(range(len(l)), range(len(l[0]))):
    if x not in explored:
        cc, perimeter = connected_component(x)
        price+= perimeter*len(cc)
        explored |= cc

price

#part 2

def has_ext_neighbours(c):
     nghbs = set((min(max(c[0] + i, 0), len(l) - 1), min(max(c[1] + j, 0), len(l[0]) - 1)) for i, j in
               product(range(-1,2),repeat=2)) - {c}

     return sum(map(lambda x: l[x[0]][x[1]] != l[c[0]][c[1]], nghbs)) > 0 or len(nghbs) < 8

def get_border(shape):
    return set(filter(has_ext_neighbours,shape))

def rotate(direction, clockwise=True):
    epsilon = 2*clockwise-1
    if direction[0]==0:
        return epsilon*direction[1], direction[0]
    return direction[1], -epsilon*direction[0]

def count_sides(border):
    x = sorted(list(border))[0]
    start = (x[0]-1, x[1])
    visited = {start}
    p = start
    nsides = 0
    d = (1,0)
    isonborder= False
    while True:
        if (p[0]+d[0], p[1]+d[1]) in border:
            r = rotate(d, clockwise=False)
            if (y:=(p[0]+r[0], p[1]+r[1])) not in border:
                p=y
            else:
                d = r
                r = rotate(r,clockwise=False)
                nsides+=1
                if (y:=(p[0]+r[0], p[1]+r[1])) not in border:
                    p = y
                else:
                    d = r
                    r = rotate(r, clockwise=False)
                    nsides+=1
                    if (y := (p[0] + r[0], p[1] + r[1])) not in border:
                        p = y
                    else:
                        nsides+=1
                        break
        else:
            p = (p[0]+d[0], p[1]+d[1])
            nsides+=1
            d = rotate(d)

        if 0<= p[0] < len(l) and 0 <= p[1] < len(l[0]):
            if get_neighbours(p) & border:
                visited.add(p)
        else:
            isonborder = True

        if p == start:
            break
    return nsides,visited, isonborder

explored,ccs, nsideslist = set(), [], []

for x in product(range(len(l)), range(len(l[0]))):
    if x not in explored:
        cc, _ = connected_component(x)
        ccs.append(cc)
        border = get_border(cc)
        nsides,visited,isonborder = count_sides(border)
        nsideslist.append(nsides)
        if not isonborder:
            for i,shape in enumerate(ccs):
                if visited & shape == visited:
                    nsideslist[i]+=nsides

        explored |= cc

sum(n*len(cc) for n,cc in zip(nsideslist,ccs))
