from functools import lru_cache
from itertools import pairwise, product

# Remark: thats the first one that I really found hard. The whole trick was to realize that 'A' is a renewal time in the sequence so that we can only focus on subpatterns
# of the form 'A*A'. A sequence is always split in subpatterns (adding a prefix A to a sequence).
# Then we compute all possible one-step-ahead images for each pattern in a sequence, and do a recursion on the new patterns created.
# Then we sum all the final results.

parse_initial_char = {
    'A': (3, 2),
    '0': (3, 1),
    '1': (2, 0),
    '2': (2, 1),
    '3': (2, 2),
    '4': (1, 0),
    '5': (1, 1),
    '6': (1, 2),
    '7': (0, 0),
    '8': (0, 1),
    '9': (0, 2)
}

parse_directional_char = {
    '^': (0, 1),
    'v': (1, 1),
    '>': (1, 2),
    '<': (1, 0),
    'A': (0, 2)
}

with open('aoc21.txt') as f:
    l = [x[:-1] for x in f.readlines()]


def get_paths(x_from, x_to, obstacles):
    if x_from == x_to:
        return ['A']

    if x_from[0] != x_to[0] and x_from[1] == x_to[1]:
        if x_to[0] > x_from[0]:
            return ['v' * (x_to[0] - x_from[0]) + 'A']
        return ['^' * (x_from[0] - x_to[0]) + 'A']

    if x_from[0] == x_to[0] and x_from[1] != x_to[1]:
        if x_to[1] > x_from[1]:
            return ['>' * (x_to[1] - x_from[1]) + 'A']
        return ['<' * (x_from[1] - x_to[1]) + 'A']

    candidates = (x_to[0], x_from[1]), (x_from[0], x_to[1])
    ret = set()

    for c in candidates:
        if c not in obstacles:
            if c[0] > x_from[0]:
                ret.add('v' * (c[0] - x_from[0]) + get_paths(c, x_to, obstacles)[0])
            elif c[0] < x_from[0]:
                ret.add('^' * (x_from[0] - c[0]) + get_paths(c, x_to, obstacles)[0])
            elif c[1] > x_from[1]:
                ret.add('>' * (c[1] - x_from[1]) + get_paths(c, x_to, obstacles)[0])
            elif c[1] < x_from[1]:
                ret.add('<' * (x_from[1] - c[1]) + get_paths(c, x_to, obstacles)[0])

    return ret


obstacles_numeric_pad = ((3, 0),)
obstacles_directional_pad = ((0, 0),)


def get_paths_sequence_directional(s):
    if len(s) <= 1:
        return {''}

    x1, x2 = parse_directional_char[s[0]], parse_directional_char[s[1]]
    return set(
        x + y for x, y in product(get_paths_sequence_directional(s[1:]), get_paths(x1, x2, obstacles_directional_pad)))


@lru_cache(maxsize=None)
def compute_minimal_length(pattern, n):
    if n == 0:
        return len(pattern) - 1

    iterated = get_paths_sequence_directional(pattern)
    nextpatterns = [['A' + x + 'A' for x in it.split('A')[:-1]] for it in iterated]
    return min([sum(compute_minimal_length(x, n - 1) for x in nnext) for nnext in nextpatterns])


def compute_minimal_length_sequence(s, n):
    return sum(compute_minimal_length(p, n) for p in ['A' + x + 'A' for x in s.split('A')[:-1]])


def compute_minimal_length_from_numerical_inputs(n):
    numeric_parse = {}
    for code in l:
        numeric_parse[code] = ['']
        for x1, x2 in pairwise(map(lambda x: parse_initial_char[x], 'A' + code)):
            numeric_parse[code] = set(
                x + y for x, y in product(numeric_parse[code], get_paths(x1, x2, obstacles_numeric_pad)))

    minlengths = {}

    for code, vals in numeric_parse.items():
        minlengths[code] = min(compute_minimal_length_sequence(s, n) for s in vals)

    return sum(minlengths[code] * int(code.replace('A', '')) for code in l)


# part 1
compute_minimal_length_from_numerical_inputs(2)

#part 2
compute_minimal_length_from_numerical_inputs(25)
