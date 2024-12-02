import numpy as np

with open('aoc2.txt') as f:
    l = [list(map(int,x.split(' '))) for x in f.readlines()]

# part 1

diffs = [set(np.diff(x)) for x in l]

len(list(filter(lambda x: x & {1,2,3} == x or x & {-1,-2,-3} == x, diffs)))

# part 2

def is_safe_diff(x):
    y = set(np.diff(x))
    return y & {1,2,3} == y or y & {-1,-2,-3} == y

def is_safe(x):
    if is_safe_diff(x):
        return True

    for i in range(len(x)):
        if is_safe_diff(x[:i]+x[i+1:]):
            return True
    return False

sum(map(is_safe, l))
