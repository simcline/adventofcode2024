import re

with open('aoc14.txt') as f:
    l = list(f.readlines())
    p_reg = re.compile('p=(-?[0-9]+),(-?[0-9]+)')
    v_reg = re.compile('v=(-?[0-9]+),(-?[0-9]+)')
    p_list = list(map(lambda x: tuple(map(int,p_reg.search(x).groups())), l))
    v_list = list(map(lambda x: tuple(map(int,v_reg.search(x).groups())), l))

#part 1

l_i = 103
l_j = 101
n = 100

def get_n(n):
    return [((p[1]+n*v[1])%l_i, (p[0]+n*v[0])%l_j ) for p,v in zip(p_list, v_list)]

final_p_list = get_n(n)
q1 = sum(p[0]<(l_i//2) and p[1]<(l_j//2) for p in final_p_list)
q2 = sum(p[0]<(l_i//2) and p[1]>(l_j//2) for p in final_p_list)
q3 = sum(p[0]>(l_i//2) and p[1]<(l_j//2) for p in final_p_list)
q4 = sum(p[0]>(l_i//2) and p[1]>(l_j//2) for p in final_p_list)

q1*q2*q3*q4

#part 2
for k in range(100000):
    f_p_list = get_n(k)
    is_symmetric = len(f_p_list) == len(set(f_p_list))

    if is_symmetric:
        break

k

