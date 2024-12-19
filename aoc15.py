from itertools import product

with open('aoc15.txt') as f:
    l = [x[:-1] for x in f.readlines()]

    w = list(map(lambda x:[y for y in x], filter(lambda x:x.startswith('#'),l)))
    instructions = ''.join(filter(lambda x:not x.startswith('#'),l))

start = [(i,j) for i,j in product(range(len(w)), range(len(w[0]))) if w[i][j] == '@'][0]

def parse_instruction(ins):
    match ins:
        case '^':
            return (-1,0)
        case '>':
            return (0,1)
        case '<':
            return (0,-1)
        case 'v':
            return (1,0)

def find_first_empty(pos,direction):
    k=1
    try:
        while True:
            c = (pos[0]+k*direction[0],pos[1]+k*direction[1])
            if w[c[0]][c[1]]=='.':
                return c, True
            if w[c[0]][c[1]]=='#':
                return None, False
            k+=1
    except IndexError:
        return None, False


instructions = list(map(parse_instruction, instructions))

pos = start
for ins in instructions:
    c,found = find_first_empty(pos,ins)
    if not found:
        continue

    k=1
    to_move = (c[0]-k*ins[0],c[1]-k*ins[1])
    while to_move[0]!=(pos[0]-ins[0]) or to_move[1]!=(pos[1]-ins[1]):
        w[c[0]-(k-1)*ins[0]][c[1]-(k-1)*ins[1]]=w[to_move[0]][to_move[1]]
        k+=1
        to_move = (c[0] - k * ins[0], c[1] - k * ins[1])

    w[pos[0]][pos[1]]= '.'
    pos = (pos[0]+ins[0], pos[1]+ins[1])


sum(i*100+j for i,j in product(range(len(w)), range(len(w[0]))) if w[i][j] == 'O')

# part 2

w = list(map(lambda x:[y for y in x], filter(lambda x:x.startswith('#'),l)))
w2 = []
for x in w:
    w2.append([])
    for y in x:
        match y:
            case '.'|'#':
                w2[-1].append(y)
                w2[-1].append(y)
            case 'O':
                w2[-1].append('[')
                w2[-1].append(']')
            case '@':
                w2[-1].append('@')
                w2[-1].append('.')

def canbepushed(pos, direction):
    nextpos = (pos[0]+direction[0], pos[1]+direction[1])
    match w2[nextpos[0]][nextpos[1]]:
        case '.':
            return True
        case '#':
            return False
        case '[':
            if direction[0] !=0:
                s1 = canbepushed(nextpos, direction)
                s2 = canbepushed((nextpos[0], nextpos[1]+1), direction)
                return s1 & s2
            return canbepushed(nextpos, direction)
        case ']':
            if direction[0] != 0:
                s1 = canbepushed(nextpos, direction)
                s2 = canbepushed((nextpos[0], nextpos[1] - 1), direction)
                return s1 & s2
            return canbepushed(nextpos, direction)

def push(pos, direction, replaceval = '.'):
    nextpos = (pos[0]+direction[0], pos[1]+direction[1])
    nextval = w2[nextpos[0]][nextpos[1]]
    match nextval:
        case '.':
            pass
        case '#':
            return
        case '[':
            if direction[0] != 0:
                push(nextpos, direction, nextval)
                push((nextpos[0], nextpos[1] + 1), direction)
            else:
                push(nextpos, direction,nextval)
        case ']':
            if direction[0] != 0:
                push(nextpos, direction, nextval)
                push((nextpos[0], nextpos[1] - 1), direction)
            else:
                push(nextpos, direction, nextval)
    w2[nextpos[0]][nextpos[1]] = w2[pos[0]][pos[1]]
    w2[pos[0]][pos[1]] = replaceval

start = [(i,j) for i,j in product(range(len(w2)), range(len(w2[0]))) if w2[i][j] == '@'][0]
pos = start
for ins in instructions:
    if not canbepushed(pos, ins):
        continue

    push( pos, ins)
    pos = (pos[0]+ins[0], pos[1]+ins[1])

    assert w2[pos[0]][pos[1]] == '@'

sum(i*100+j for i,j in product(range(len(w2)), range(len(w2[0]))) if w2[i][j] == '[')