import itertools
from functools import reduce
import operator

bot_map = {
    '1000':[0],
    '1100':[0],
    '1010':[0],
    '1110':[0,1],
    '1111':[0],
}

def main(height,has_type):
    has_int = int(has_type[::-1],base=2)
    one_layer = [i for i in range(1<<4) if (i | has_int) == has_int]
    top_layer = [i for i in one_layer if i != 0]
    bot_layer = [1<<i for i in bot_map[has_type]]
    all_comb = [bot_layer] + [one_layer] * (height-2) + [top_layer]
    data = list(itertools.product(*all_comb))
    data = [t for t in data if reduce(operator.or_, t) == has_int]
    data = [tuple(bin(x)[2:].zfill(4)[::-1] for x in t) for t in data]
    data = ["\n".join(["".join([i[x] for i in t]) for x in range(4)]) for t in data]
    content=str(len(data))+"\n\n"+"\n\n".join(data)
    filename = f"data/{has_type}_{height}.txt"
    with open(filename,"w") as f:
        f.write(content)

if __name__=='__main__':
    lst=[]
    for i in range(2,7):
        for j in ["1000","1100","1010","1110","1111"]:
            lst.append((i,j))
    for i,j in lst:
        main(i,j)