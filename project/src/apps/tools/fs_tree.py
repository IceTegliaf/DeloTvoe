import os

class FSTreePath(object):
    CODE_DICT = "0123456789abcdefghijklmnopqrstuvwxyz"
    
    def __init__(self, root, letter_per_dir=2, max_level=2):
        self.letter_per_dir = letter_per_dir
        self.max_level = max_level
        self.base = self.letter_per_dir*self.max_level
        self.size = len(FSTreePath.CODE_DICT)
        self.root = root
        
    def _int2code(self, i):        
        maximum = pow(self.size, self.base)
        #normalize
        i = divmod(i, maximum)[1]
        
        res = ""
        while i>0 or res=="":
            i1,i2 = divmod(i, self.size)
            res=res+FSTreePath.CODE_DICT[i2]
            i=i1
            
        while len(res)<self.base: 
            res=res+FSTreePath.CODE_DICT[0]
        return res
        
    def _int2list(self, i):
        code = self._int2code(i)
        res=[]
        while code:
            res.append(code[:self.letter_per_dir])
            code = code[self.letter_per_dir:]
        return res
    
    def get_or_create(self, i):
        path_list = self._int2list(i)
        path = self.root
        for name in path_list:
            path = os.path.join(path, name)
            if not os.path.exists(path):
                os.mkdir(path)
        return path
                    
        
        