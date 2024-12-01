with open('aoc1.txt') as f:
    l = [x.split('   ') for x in f.readlines()]

#part 1
l1, l2 = sorted(list(map(lambda x: int(x[0]), l))), sorted(list(map(lambda x: int(x[1][:-1]), l)))

sum(abs(y - x) for x, y in zip(l1, l2))

#part 2

sum(len([x for x in l2 if x == y]) * y for y in l1)
