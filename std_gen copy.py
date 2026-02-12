import pickle
import numpy as np
from pathlib import Path
from utils import Shape

def memoize(func):
    def wrapper(self, state ,load = True):
        if load:
            key = self._key(state)
            if key in self.cache:
                return self.cache[key]
        result = func(self, state,load)
        # self.cache[key] = result
        return result
    return wrapper

class StateChecker:
    def __init__(self, cache_file="state_cache.pkl"):
        self.cache_file = Path(cache_file)
        self.cache = self._load_cache()

    def _load_cache(self):
        if self.cache_file.exists():
            with open(self.cache_file, "rb") as f:
                return pickle.load(f)
        return {}

    def save_cache(self):
        with open(self.cache_file, "wb") as f:
            pickle.dump(self.cache, f)

    def _key(self, state):
        return self._normalize(state).tobytes()
    
    def _normalize(self, state:Shape):
        candidates = []
        for sta in [state,state.mirror()]:
            for i in range(4):
                candidates.append(sta.rotate(shift=i))
        return min(candidates,key=lambda x:x.tobytes())

    @memoize
    def is_reachable(self, state:Shape, load = True):
        state=state.fall_and_shrink()
        if state.get_row_popcount(0)>=2:
            return True
        bitmask = state.to_bitmask()
        if any(bitmask[i] == 0 and bitmask[(i+1) % 4] == 0 for i in range(4)):
            return True
        # print(state)
        prime_col_id = np.nonzero(state[:,0])[0]
        for split_col_id in range(4):
            cand = state.match(lambda wd:wd[split_col_id,:].all(),width=2)
            # print(cand)
            for mask in range(1<<4): # lower 
                if mask>>split_col_id&1:
                    continue
                if prime_col_id != split_col_id and not mask>>prime_col_id&1:
                    continue
                # print(mask)
                if mask.bit_count()==1: # cnt(lower) == 2
                    continue
                lower_col_mask = (mask>>np.arange(4)&1) == 1
                upper_col_mask = ~lower_col_mask
                upper_col_mask[split_col_id] = False
                lower = state.copy()
                lower[~lower_col_mask,:] = 0
                upper = state.copy()
                upper[~upper_col_mask,:] = 0
                for row_id in cand:
                    lower[split_col_id,:] = 0
                    lower[split_col_id,:row_id+1] = state[split_col_id,:row_id+1]
                    upper[split_col_id,:] = 0
                    upper[split_col_id,row_id+1:] = state[split_col_id,row_id+1:]
                    # print(state,lower,upper)
                    if self.is_reachable(lower) and self.is_reachable(upper):
                        # if load==False:
                        #     print(upper,lower)
                        return True
                    
        return False

if __name__ == "__main__":

    checker = StateChecker()

    data ='''
10010011
00001000
00000011
01000000
'''
    state=Shape(data.strip().split('\n'))
    print(checker.is_reachable(state,load=False))
    exit()

    pat = ["1000","1100","1010","1110","1111"]
    file_names = [f"{x}_{y}" for x in pat for y in range(6,7)]

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
                result = checker.is_reachable(state,load=False)
                outs.write("\n"*5)
                outs.write('y' if result else 'n')

    # checker.save_cache()
