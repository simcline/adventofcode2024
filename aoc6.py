from itertools import product

with open('aoc6.txt') as f:
    l = [x[:-1] for x in f.readlines()]

#part 1

obstacles = []
start=(0,0)
for i,j in product(range(len(l)), range(len(l[0]))):
    if l[i][j]=='#':
        obstacles.append((i, j))
    if l[i][j]=='^':
        start=(i,j)

path = {start}
out = False
direction = (-1,0)
position=start

def nextpos(pos, direction):
    return pos[0] + direction[0], pos[1] + direction[1]

def isout(position):
    return position[0]<0 or position[0]>=len(l) or position[1]<0 or position[1]>=len(l[0])

def rotate(direction):
    if direction[0]==0:
        return direction[1], direction[0]
    return direction[1], -direction[0]

while not out:
    nxtpos = nextpos(position, direction)
    out=isout(nxtpos)
    if not out:
        if nxtpos in obstacles:
            direction = rotate(direction)
        else:
            path.add(nxtpos)
            position = nxtpos

len(path)

#part 2

def ends_in_loop(newobstacle):
    direction = (-1,0)
    path = {(start, direction)}
    position=start
    newobstacles = obstacles+[newobstacle]
    while True:
        nxtpos = nextpos(position, direction)
        if isout(nxtpos):
            return False
        if nxtpos in newobstacles:
            direction = rotate(direction)
        else:
            if (nxtpos, direction) in path:
                return True
            path.add((nxtpos, direction))
            position = nxtpos

#This is somewhat brute force and takes a few minutes, but works...
sum(map(ends_in_loop, path - {start}))

