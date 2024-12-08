with open('aoc7.txt') as f:
    l = [x[:-1] for x in f.readlines()]

res = list(map(lambda x: int(x.split(':')[0]), l))
inputs = list(map(lambda x: [int(y) for y in x.split(':')[1].split(' ') if y != ''], l))

#part 1

def check(res, input):
    if len(input)==1:
        return res==input[0]
    else:
        return check(res-input[-1], input[:-1]) or (res % input[-1] ==0 and check(res//input[-1], input[:-1]))

sum(r*check(r,i) for r,i in zip(res, inputs))

#part 2

def check2(res, input):
    if len(input)==1:
        return res==input[0]
    else:
        last_str = str(input[-1])
        return (
                check2(res-input[-1], input[:-1])
                or (res % input[-1] == 0 and check2(res//input[-1], input[:-1]))
                or (str(res)[-len(last_str):] == last_str and check2(int(str(res)[:(-len(last_str))]), input[:-1]))
                )

sum(r*check2(r,i) for r,i in zip(res, inputs))