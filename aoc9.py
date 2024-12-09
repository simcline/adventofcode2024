with open('aoc9.txt') as f:
    l = list(map(int,f.readline()[:-1]))

types = []

for i in range(len(l)):
    if i%2==1:
        types.append('F')
    else:
        types.append(i//2)

#part 1

firstfree = 1
keepgoing = True
while keepgoing:
    if l[firstfree] < l[-1]:
        types[firstfree] = types[-1]
        l[-1] -= l[firstfree]
        firstfree +=1
        while firstfree < len(l) and types[firstfree] != 'F':
            firstfree+=1
    else:
        if l[firstfree] == l[-1]:
            types[firstfree] = types[-1]
        else:
            l.insert(firstfree, l[-1])
            types.insert(firstfree, types[-1])
            l[firstfree+1] -= l[-1]
            firstfree +=1

        while firstfree < len(l) and types[firstfree] != 'F':
            firstfree+=1
        del l[-1], types[-1]
        while types[-1] == 'F':
            del l[-1], types[-1]
    keepgoing = firstfree < len(l)

def checksum(l,t):
    s = 0
    cs = 0
    for i in range(len(l)):
        if t[i]!='F':
            s+= t[i]*sum(range(cs, cs+l[i]))
        cs+= l[i]
    return s

checksum(l,types)

#part 2

with open('aoc9.txt') as f:
    l = list(map(int,f.readline()[:-1]))

types = []

for i in range(len(l)):
    if i%2==1:
        types.append('F')
    else:
        types.append(i//2)

firstfree = 1
lastfile = len(l)-1
keepgoing = True
while keepgoing:
    if l[firstfree] < l[lastfile]:
        firstfree +=1
        while firstfree <= lastfile and types[firstfree] != 'F':
            firstfree+=1
    else:
        if l[firstfree] == l[lastfile]:
            types[firstfree] = types[lastfile]
            types[lastfile] = 'F'
            lastfile -= 1
        else:
            to_insert_type = types[lastfile]
            types[lastfile] = 'F'
            l[firstfree] -= l[lastfile]
            l.insert(firstfree, l[lastfile])
            types.insert(firstfree, to_insert_type)

        while types[lastfile] == 'F':
            lastfile -= 1

        firstfree = 0
        while firstfree < lastfile and types[firstfree] != 'F':
            firstfree+=1

    while firstfree >= lastfile >= 0:
        lastfile -= 1
        while lastfile >=0 and types[lastfile] == 'F':
            lastfile -= 1
        firstfree = 0
        while firstfree < lastfile and types[firstfree] != 'F':
            firstfree+=1

    keepgoing = lastfile > -1

checksum(l,types)

