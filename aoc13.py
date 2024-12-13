import re
e1_reg = re.compile('Button A: X\+([0-9]+), Y\+([0-9]+)')
e2_reg = re.compile('Button B: X\+([0-9]+), Y\+([0-9]+)')
dest_reg = re.compile('Prize: X=([0-9]+), Y=([0-9]+)')

e1list, e2list, destslist = [],[],[]
with open('aoc13.txt') as f:
    for x in f.readlines():
        m1 = re.match(e1_reg, x)
        if m1:
            e1list.append( tuple(map(int, m1.groups(1))))
            continue
        m2 = re.match(e2_reg, x)
        if m2:
            e2list.append( tuple(map(int, m2.groups(1))))
            continue
        m3 = re.match(dest_reg, x)
        if m3:
            destslist.append( tuple(map(int, m3.groups(1))))

def getntokens(K):
    ntokens = 0
    for e1,e2,dest in zip(e1list,e2list,destslist):
        mdest = (dest[0]+K, dest[1]+K)
        detM = e1[0]*e2[1]-e1[1]*e2[0]
        if detM==0:
            continue

        s1,s2 = (e2[1]*mdest[0] - e2[0]*mdest[1])//detM, (-e1[1]*mdest[0]+e1[0]*mdest[1])//detM

        if any((s1*e1[0]+s2*e2[0]!=mdest[0],
                s1*e1[1]+s2*e2[1]!=mdest[1],
                s1 <0, s2 <0,
                (K==0 and (s1 >100 or s2 >100)))):
            continue

        ntokens += 3*s1+s2
    return ntokens

#part 1
getntokens(0)

#part 2
getntokens(10000000000000)