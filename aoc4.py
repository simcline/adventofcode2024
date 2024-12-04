import re
from functools import reduce
from itertools import product, starmap
with open('aoc4.txt') as f:
    l = [x[:-1] for x in f.readlines()]

#part 1

reg = re.compile('XMAS')
n = len(l)
l_cols = [reduce(lambda x, y: x + y, [l[i][k] for i in range(n)] ) for k in range(len(l[0]))]
l_diags = [reduce(lambda x, y: x + y, [l[i][i+k] for i in range(max(-k,0), min(n, n-k))] ) for k in range(-len(l[0])+1, len(l[0]) )]
l_codiags = [reduce(lambda x, y: x + y, [l[n-1-i][i+k] for i in range(max(-k,0), min(n, n-k))] ) for k in range(-len(l[0])+1, len(l[0]) )]

res=sum(len(re.findall(reg, row)) for row in l)
res+=sum(len(re.findall(reg, row[::-1])) for row in l)
res+=sum(len(re.findall(reg, col)) for col in l_cols)
res+=sum(len(re.findall(reg, col[::-1])) for col in l_cols)
res+=sum(len(re.findall(reg, diag)) for diag in l_diags)
res+=sum(len(re.findall(reg, diag[::-1])) for diag in l_diags)
res+=sum(len(re.findall(reg, diag)) for diag in l_codiags)
res+=sum(len(re.findall(reg, diag[::-1])) for diag in l_codiags)

res

# part 2

def is_cross(i,j):
    if l[i][j] != 'A':
        return False

    diag_ok = (l[i-1][j-1] == 'M' and l[i+1][j+1] == 'S') or (l[i-1][j-1] == 'S' and l[i+1][j+1] == 'M')
    codiag_ok = (l[i-1][j+1] == 'M' and l[i+1][j-1] == 'S') or (l[i-1][j+1] == 'S' and l[i+1][j-1] == 'M')
    return diag_ok and codiag_ok

sum(starmap(is_cross,product(range(1,n-1), repeat=2)))