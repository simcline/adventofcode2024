import re
from functools import reduce

with open('aoc3.txt') as f:
    l = f.readlines()

l=reduce(lambda x,y: x+y, l)

#part 1

reg = re.compile('mul\(([0-9]+),([0-9]+)\)')
sum(int(x[0])*int(x[1]) for x in reg.findall(l))

#part 2

enabled=True
res=0
while len(l):
    if enabled:
        head, _, tail= l.partition('don\'t()')
        res+= sum(int(x[0])*int(x[1]) for x in reg.findall(head))
    else:
        _, _, tail = l.partition('do()')
    enabled= not enabled
    l=tail
res