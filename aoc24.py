import re

gate_reg = re.compile('([a-z0-9]+) (OR|AND|XOR) ([a-z0-9]+) -> ([a-z0-9]+)')

wire_values = {}

with open('aoc24.txt') as f:
    iv = [x[:-1].split(':') for x in f.readlines() if ':' in x]
    for x in iv:
        wire_values[x[0]] = int(x[1][1:])

with open('aoc24.txt') as f:
    gates = []
    for x in f.readlines():
        if mtch:=gate_reg.match(x):
            grps = mtch.groups()
            gates.append(grps)
            for w in (grps[0], grps[2], grps[3]):
                if w not in wire_values:
                    wire_values[w] = None

def do_gate(g):
    if wire_values[g[0]] is not None and wire_values[g[2]] is not None:
        match g[1]:
            case 'OR':
                wire_values[g[3]] = wire_values[g[0]] | wire_values[g[2]]
            case 'AND':
                wire_values[g[3]] = wire_values[g[0]] & wire_values[g[2]]
            case 'XOR':
                wire_values[g[3]] = wire_values[g[0]] ^ wire_values[g[2]]

#part 1

def compute():
    while any([z is None and w.startswith('z') for w,z in wire_values.items()]):
        for g in gates:
            do_gate(g)

    res = 0
    for w in wire_values:
        if w.startswith('z'):
            res += wire_values[w]*(2**int(w[1:]))
    return res

compute()

#part 2
# Remark, for this one I relabelled progressively all the wires with their sum and carry function in the adder units.
# Everytime the relabelling process stops, it means that something is wrong and
# I manually look up where it stops, and deduce which two gates should be swapped for the labelling process to continue.


class Gate:
    def __init__(self, g, id):
        self.left = g[0]
        self.right = g[2]
        self.op = g[1]
        self.out = g[3]
        self.id = id

    def __repr__(self):
        return f'{self.left} {self.op} {self.right} -> {self.out}'

    def __contains__(self, item):
        return item in (self.left, self.out, self.right)

    def __clone__(self):
        return Gate((self.left, self.op, self.right, self.out), self.id)

gs_raw = list(map(lambda e: Gate(e[1],e[0]), enumerate(gates)))
def label_wires(gs):
    gs = list(map(lambda x: x.__clone__(), gs))
    replace_dico = {}

    for g in gs:
        if (g.left[0] == 'x' and g.right[0] == 'y') or (g.left[0] == 'y' and g.right[0] == 'x') and g.left[1:] == g.right[1:]:
            if g.op == 'XOR':
                if int(g.left[1:]) == 0:
                    replace_dico[g.out] = g.out
                else:
                    replace_dico[g.out] = 'ISUM'+g.left[1:]
            elif g.op == 'AND':
                if int(g.left[1:]) == 0:
                    replace_dico[g.out] = 'CARRY'+g.left[1:]
                else:
                    replace_dico[g.out] = 'ICARRY' + g.left[1:]
            g.out = replace_dico[g.out]

    for g in gs:
        g.left = replace_dico.get(g.left, g.left)
        g.right = replace_dico.get(g.right, g.right)
        g.out = replace_dico.get(g.out, g.out)

    while True:
        k = len(replace_dico)
        print(f'{k=}')
        for g in gs:
            if g.left[:5] == 'CARRY' and g.right[:4] == 'ISUM' and int(g.left[5:]) + 1 == int(g.right[4:]) and g.op == 'AND':
                replace_dico[g.out] = 'COCARRY'+g.right[4:]
                g.out = replace_dico[g.out]
            elif g.right[:5] == 'CARRY' and g.left[:4] == 'ISUM' and int(g.right[5:]) + 1 == int(g.left[4:]) and g.op == 'AND':
                replace_dico[g.out] = 'COCARRY'+g.left[4:]
                g.out = replace_dico[g.out]

        for g in gs:
            g.left = replace_dico.get(g.left, g.left)
            g.right = replace_dico.get(g.right, g.right)
            g.out = replace_dico.get(g.out, g.out)

        for g in gs:
            if g.left[:7] == 'COCARRY' and g.right[:6] == 'ICARRY' and g.left[7:] == g.right[6:] and g.op == 'OR':
                replace_dico[g.out] = 'CARRY'+g.right[6:]
                g.out = replace_dico[g.out]
            elif g.right[:7] == 'COCARRY' and g.left[:6] == 'ICARRY' and g.right[7:] == g.left[6:] and g.op == 'OR':
                    replace_dico[g.out] = 'CARRY' + g.left[6:]
                    g.out = replace_dico[g.out]

        for g in gs:
            g.left = replace_dico.get(g.left, g.left)
            g.right = replace_dico.get(g.right, g.right)
            g.out = replace_dico.get(g.out, g.out)

        if len(replace_dico) == k:
            break

    return replace_dico, gs

swapped = []
def swap(g1,g2):
    g1.out, g2.out = g2.out, g1.out
    swapped.extend([g1.out,g2.out])

replace_dico, gs = label_wires(gs_raw)

issue0 = (list(filter(lambda g: g.left[:5] == 'CARRY' and g.right[:4] == 'ISUM' and int(g.left[5:]) + 1 == int(g.right[4:]) and g.op == 'XOR' and g.out[0]!='z', gs))+
 list(filter(lambda g: g.right[:5] == 'CARRY' and g.left[:4] == 'ISUM' and int(g.right[5:]) + 1 == int(g.left[4:]) and g.op == 'XOR' and g.out[0]!='z', gs)))[0]
issue1 = list(filter(lambda g: replace_dico['z'+issue0.right[-2:]] in g, gs))[0]

swap(gs_raw[issue0.id], gs_raw[issue1.id])

replace_dico, gs = label_wires(gs_raw)

issue0 = (list(filter(lambda g: g.left[:5] == 'CARRY' and g.right[:4] == 'ISUM' and int(g.left[5:]) + 1 == int(g.right[4:]) and g.op == 'XOR' and g.out[0]!='z', gs))+
 list(filter(lambda g: g.right[:5] == 'CARRY' and g.left[:4] == 'ISUM' and int(g.right[5:]) + 1 == int(g.left[4:]) and g.op == 'XOR' and g.out[0]!='z', gs)))[0]
issue1 = list(filter(lambda g: replace_dico['z'+issue0.right[-2:]] in g, gs))[0]

swap(gs_raw[issue0.id], gs_raw[issue1.id])

replace_dico, gs = label_wires(gs_raw)

issue0 = list(filter(lambda g: g.out == 'ICARRY30', gs))[0]
issue1 = list(filter(lambda g: g.out == 'ISUM30', gs))[0]

swap(gs_raw[issue0.id], gs_raw[issue1.id])

replace_dico, gs = label_wires(gs_raw)

issue0 = (list(filter(lambda g: g.left[:5] == 'CARRY' and g.right[:4] == 'ISUM' and int(g.left[5:]) + 1 == int(g.right[4:]) and g.op == 'XOR' and g.out[0]!='z', gs))+
 list(filter(lambda g: g.right[:5] == 'CARRY' and g.left[:4] == 'ISUM' and int(g.right[5:]) + 1 == int(g.left[4:]) and g.op == 'XOR' and g.out[0]!='z', gs)))[0]
issue1 = list(filter(lambda g: replace_dico['z'+issue0.right[-2:]] in g, gs))[0]

swap(gs_raw[issue0.id], gs_raw[issue1.id])

','.join(sorted(swapped))