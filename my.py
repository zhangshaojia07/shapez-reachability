from utils import Shape
from pathlib import Path

# a=Shape("a","b","c","d")
# a[1,0]=6
# print(b:=a.rotate("left",1))
# print(a)
# c=a.stack_on(b)
# print(c)
# d=c.cut()
# print(d)
# d=d.stack_on(d)
# d[:,-1]=0
# print(d)
# d=d.fall_and_shrink()
# print(d)

def seg_bot(state:Shape,col_id,x):
    return state[col_id,x]>0 and (state.get_col_first_set(col_id)==x or state[col_id,x-1])

def is_reachable(state:Shape):
    cand = [state.rotate(shift=i) for i in range(4)]
    cand = [(st,[1 if i>0 else 0 for i in st.to_bitmask()]) for st in cand]
    state,bitmask = max(cand,key=lambda x:x[1])
    if bitmask in [[1,0,0,0],[1,1,0,0]]:
        return True
    elif bitmask in [[1,0,1,0]]:
        for i in range(state.n):
            if seg_bot(state,0,i) and seg_bot(state,2,i):
                return True
        return False
    elif bitmask in [[1,1,1,0]]:

        if len(state.match(lambda wd:wd[1,:].all(),width=2))>0:
            return True
        
        lim = state.n
        for i in range(3):
            cur = -1
            for j in range(state.n):
                if seg_bot(state,i,j):
                    cur = j
            lim = min(lim,cur)
        for i in range(lim+1):
            if sum(seg_bot(state,j,i) for j in [0,1,2])>=2:
                return True
            
        for i in range(state.n):
            if seg_bot(state,0,i) and seg_bot(state,2,i):
                if state.get_col_first_set(0)!=i or state.get_col_first_set(2)!=i:
                    return True
            
        return False
    elif bitmask in [[1,1,1,1]]:
        return True
    else:
        raise NotImplementedError()

if __name__ == "__main__":

    pat = [
        "1000",
        "1100",
        "1010",
        "1110",
        # "1111",
           ]
    file_names = [f"{x}_{y}" for x in pat for y in range(2,7)]

    for file_name in file_names:

        print(f"working on {file_name}")

        input_file = Path(f"data/{file_name}.txt")
        output_file = Path(f"output/{file_name}_my.txt")

        with open(input_file,"r") as ins:
            content = ins.readlines()
            n = int(content[0])
            content = [s.strip() for s in content]
            content = [s for s in content[1:] if s != ""]
            content = [content[i:i+4] for i in range(0, len(content), 4)]

        with open(output_file,"w") as outs:
            for test_case in content:
                state = Shape(test_case)
                result = is_reachable(state)
                outs.write("\n"*5)
                outs.write('y' if result else 'n')