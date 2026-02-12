import numpy as np

class Shape:
    
    def __init__(self, *args):
        if not args:
            str_data=("","","","")
        elif len(args) == 1 and isinstance(args[0], (tuple, list)):
            str_data = tuple(args[0])
        else:
            str_data = args
        self.n = max(len(col) for col in str_data)
        str_data = [col[::-1].zfill(self.n)[::-1] for col in str_data]
        self._data = np.empty((4, self.n), dtype=np.uint8)
        for col_id in range(4):
            for i in range(self.n):
                self._data[col_id,i]=int(str_data[col_id][i],16)
    
    @staticmethod
    def col2str(col):
        return "".join(f"{i:x}" for i in col)

    def __repr__(self):
        return f"Shape(n={self.n}, cols=[\n{",\n".join(['\"'+self.col2str(self._data[i])+'\"' for i in range(4)])}])"
    
    def __getitem__(self,key):
        return self._data[key]
    
    def __setitem__(self,key,value):
        self._data[key]=value

    def copy(self):
        new_obj = self.__class__.__new__(self.__class__)
        new_obj.n = self.n
        new_obj._data = self._data.copy()
        return new_obj

    def tobytes(self):
        return self._data.tobytes()
    
    def get_col_first_set(self,col_id):
        col = self._data[col_id]
        nonzero = np.nonzero(col)[0]
        return nonzero[0] if len(nonzero) > 0 else self.n
    
    def get_col_last_set(self,col_id):
        col = self._data[col_id]
        nonzero = np.nonzero(col)[0]
        return nonzero[-1] if len(nonzero) > 0 else -1
    
    def get_col_popcount(self,col_id):
        return np.count_nonzero(self._data[col_id])
    
    def get_row_popcount(self,col_id):
        return np.count_nonzero(self._data[:,col_id])
    
    def match(self,condition,width=2):
        ret = []
        for row in range(self.n - width + 1):
            window = self._data[:,row:row+width]
            if condition(window):
                ret.append(row)
        return ret
    
    def fall_and_shrink(self):
        offset_l = min(self.get_col_first_set(i) for i in range(4))
        offset_r = max(self.get_col_last_set(i) for i in range(4))
        
        new_obj = self.__class__.__new__(self.__class__)
        new_obj.n = offset_r+1-offset_l
        new_obj._data = self._data[:,offset_l:offset_r+1]
        return new_obj
    
    def to_bitmask(self):
        result = [0, 0, 0, 0]
        for i in range(4):
            for j in range(self.n):
                if self._data[i, j]:
                    result[i] |= (1 << j)
        return result
    
    def stack_on(self,other):
        if not isinstance(other,Shape):
            raise TypeError("Shape stack on non-Shape")
        
        ctz = [self.get_col_first_set(i) for i in range(4)]
        offset = max(other.get_col_last_set(i)+1-ctz[i] for i in range(4))

        new_obj = self.__class__.__new__(self.__class__)
        new_obj.n = self.n + offset
        stacked_data = np.zeros((4, new_obj.n), dtype=np.uint8)
        stacked_data[:,:other.n] = other._data
        for i in range(4):
            stacked_data[i,offset+ctz[i]:offset+self.n] = self._data[i,ctz[i]:]

        new_obj._data = stacked_data
        return new_obj

    def rotate(self,direction='left',shift:int=1):
        if direction not in ('left', 'right'):
            raise ValueError("direction must be either 'left' or 'right'")
        
        new_obj = self.__class__.__new__(self.__class__)
        new_obj.n = self.n
        
        if direction == 'left':
            rotated_data = np.roll(self._data, -shift, axis=0)
        else:  # 'right'
            rotated_data = np.roll(self._data, shift, axis=0)

        new_obj._data = rotated_data
        return new_obj
    
    def mirror(self):
        new_obj = self.__class__.__new__(self.__class__)
        new_obj.n = self.n
        mirrored_data = self._data.copy()
        mirrored_data[[1, 3], :] = mirrored_data[[3, 1], :].copy()
        new_obj._data = mirrored_data
        return new_obj
    
    def cut(self,mask='1100'):
        if isinstance(mask,str):
            mask=int(mask[::-1],base=2)
        new_obj = self.__class__.__new__(self.__class__)
        new_obj.n = self.n
        new_obj._data = self._data.copy()
        for i in range(4):
            if not mask>>i&1:
                new_obj._data[i,:] = 0
        return new_obj