from collections import defaultdict

with open('aoc11.txt') as f:
    l = f.readline()[:-1]

def get_number_stones(n):
    d = defaultdict(lambda :0)
    for x in map(int,l.split(' ')):
        d[x] += 1

    for i in range(n):
        nextd = defaultdict(lambda :0)
        for s,v in d.items():
            match s:
                case 0:
                    nextd[1]+=d[s]
                case _ if len(str(s)) % 2 == 0:
                    str_s = str(s)
                    left,right = int(str_s[:(len(str_s) // 2)]), int(str_s[(len(str_s) // 2):])
                    nextd[left]+=d[s]
                    nextd[right]+=d[s]
                case _:
                    nextd[s * 2024]+=d[s]
        d=nextd

    return sum(d.values())

#part 1
get_number_stones(25)

#part 2
get_number_stones(75)
