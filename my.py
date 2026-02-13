from utils import Shape
from pathlib import Path
import bisect

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

        cand = [state.rotate(shift=i) for i in range(4)]
        state = [i for i in cand if i[0,0]>0][0]

        eq_pos = [state.match(lambda wd:wd[i,:].all(),width=2) for i in range(4)] # row_id of lower
        seg_pos = [[j for j in range(state.n) if seg_bot(state,i,j)] for i in range(4)]

        idx = list(range(4))

        op_idx = [(0,2),(1,3)]

        two_idx = [(j,i) for i in range(4) for j in range(i)]

        for i,j in zip(idx,idx[1:]+idx[:1]):
            if len(eq_pos[i])>0 and len(eq_pos[j])>0:
                return True
        
        for i,j in op_idx:
            if set(eq_pos[i]) & set(eq_pos[j]):
                return True

        lim = state.n
        for i in range(4):
            cur = -1
            for j in range(state.n):
                if seg_bot(state,i,j):
                    cur = j
            lim = min(lim,cur)
        for i in range(lim+1):
            if sum(seg_bot(state,j,i) for j in range(4))>=2:
                return True

        for x,y in op_idx:
            for i in range(state.n):
                if seg_bot(state,x,i) and seg_bot(state,y,i):
                    if state.get_col_first_set(x)!=i or state.get_col_first_set(y)!=i:
                        if any(map(lambda k:k>=i,eq_pos[x])) or any(map(lambda k:k>=i,eq_pos[y])):
                            return True

        for x,y in op_idx:
            for i in range(state.n):
                if seg_bot(state,x,i) and seg_bot(state,y,i):
                    if x!=2 and any(map(lambda k:k<=i-2,eq_pos[x])):
                        return True
                    if y!=2 and any(map(lambda k:k<=i-2,eq_pos[y])):
                        return True
        
        for x,y in two_idx:
            z,w = set(range(4)) - {x,y}
            for i in range(state.n):
                if seg_bot(state,x,i) and seg_bot(state,y,i):
                    for _ in range(2):
                        # z is the last col
                        if z!=0:
                            if (pos:=bisect.bisect_left(seg_pos[w],i))!=len(seg_pos[w]):
                                pos = seg_pos[w][pos]
                                if (z&1)!=(w&1) and any(map(lambda k:k>=pos,eq_pos[w])):
                                    return True
                                if (z&1)!=(x&1) and any(map(lambda k:k>=i,eq_pos[x])):
                                    return True
                                if (z&1)!=(y&1) and any(map(lambda k:k>=i,eq_pos[y])):
                                    return True
                        z,w = w,z

        for x,y,z in zip(idx,idx[1:]+idx[:1],idx[2:]+idx[:2]):
            lim = state.n
            for i in [x,y,z]:
                cur = -1
                for j in range(state.n):
                    if seg_bot(state,i,j):
                        cur = j
                lim = min(lim,cur)
            for i in range(lim+1):
                lst = [seg_bot(state,j,i) for j in [x,y,z]]
                if sum(lst)>=2:
                    if lst[1]:
                        if lst[2] and len(eq_pos[x])>0 and eq_pos[x][-1]>=i-1:
                            return True
                        if lst[0] and len(eq_pos[z])>0 and eq_pos[z][-1]>=i-1:
                            return True
                    for k in [x,z]:
                        if i-1 in eq_pos[k]:
                            return True


        return False
    else:
        raise NotImplementedError()

if __name__ == "__main__":

    pat = [
        "1000",
        "1100",
        "1010",
        "1110",
        "1111",
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