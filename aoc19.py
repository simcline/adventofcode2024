from functools import lru_cache

with open('aoc19.txt') as f:
    patterns = f.readline()[:-1].split(', ')
    f.readline()
    designs = [x[:-1] for x in f.readlines()]

@lru_cache(maxsize=None)
def parse(design):
    if design == '':
        return 1

    n_parsed = 0
    for x in patterns:
        if design.startswith(x):
            n_parsed += parse(design[len(x):])
    return n_parsed

#part 1
sum(map(lambda x: parse(x)>0, designs))

#part 2
sum(map(parse, designs))
