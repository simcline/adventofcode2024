from itertools import product

with open('aoc25.txt') as f:
    l = [x[:-1] for x in f.readlines()]

locks = []
keys = []

new_item = True
item_type = 'lock'
for x in l:
    if x == '':
        if item_type  == 'lock':
            locks.append(item)
        else:
            keys.append(item)
        new_item = True
        continue

    if new_item:
        item = [0] * len(x)
        item_type = 'lock' if '#' in x else 'key'
        new_item = False
    for i, c in enumerate(x):
        item[i] += c == '#'

if item_type  == 'lock':
    locks.append(item)
else:
    keys.append(item)

sum(all([x+y<=7 for x,y in zip(key,lock)]) for key,lock in product(keys, locks))