from itertools import product

class State:
    def __init__(self, ra,rb,rc):
        self.i=0
        self.ra=ra
        self.rb=rb
        self.rc=rc
        self.output=[]
        self.jumped=False

    def run(self, prog, stopatjump=False):
        self.i=0
        self.output = []
        self.jumped=False
        while self.i<len(prog):
            instructions[prog[self.i]](self, prog[self.i+1])
            if stopatjump and self.jumped:
                return
            if not self.jumped:
                self.i+=2
            self.jumped=False

with open('aoc17.txt') as f:

    ra = int(f.readline().split(' ')[-1])
    rb = int(f.readline().split(' ')[-1])
    rc = int(f.readline().split(' ')[-1])
    f.readline()
    prog = list(map(int, f.readline()[:-1].split(' ')[-1].split(',')))
    state = State(ra,rb,rc)

def combo(state,oper):
    if oper<=3:
        return oper
    match oper:
        case 4:
            return state.ra
        case 5:
            return state.rb
        case 6:
            return state.rc

def adv(state,oper):
    state.ra //= (2 ** combo(state, oper))

def bxl(state,oper):
    state.rb ^= oper

def bst(state,oper):
    state.rb = combo(state,oper) % 8

def jnz(state,oper):
    if state.ra==0:
        return
    state.i = oper
    state.jumped=True

def bxc(state,oper):
    state.rb ^= state.rc

def out(state,oper):
    state.output.append(combo(state,oper) % 8)

def bdv(state,oper):
    state.rb = state.ra//(2 ** combo(state, oper))

def cdv(state,oper):
    state.rc = state.ra//(2 ** combo(state, oper))

instructions = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv
}

#part 1

state.run(prog)
print(','.join(map(str,state.output)))


#part 2

def solution(p=prog, prog=prog):

    candidates = [[0]]

    for k in range(len(p)):
        candidates.append([])
        cnd = candidates[-2]
        for c,x in product(cnd, range(8)):
                testra = c * 8 + x
                state.ra = testra
                state.run(prog, stopatjump=True)
                if state.output[0] == p[-1-k]:
                    candidates[-1].append(testra)

    return min(candidates[-1])

solution()
