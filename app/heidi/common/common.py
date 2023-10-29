import math
from app.heidi.subspace.api import subsets
from heidi.database.database import *

def get_bit_map(dims):
    """
    Return a bit map for a given number of dimensions.
    """
    max_count=int(math.pow(2,dims))
    allsubspaces=range(1,max_count)
    f=lambda a:sorted(a,key=lambda x:sum(int(d)for d in bin(x)[2:]))
    allsubspaces=f(allsubspaces)
    #print(allsubspaces)
    frmt=str(dims)+'b'
    factor=1
    bit_map={}
    subspace_map={}
    count=0
    for i in allsubspaces:
        bin_value=str(format(i,frmt))
        subspace_col=[index for index,value in enumerate(bin_value) if value=='1']
        #print(count,tuple(subspace_col))
        subspace_map[tuple(subspace_col)]=count
        t=list(subsets(subspace_col))[1:]
        bit_map[count]=t
        count += 1
    bit_map1={}
    for i in bit_map:
        t=[]
        for val in bit_map[i]:
            t.append(subspace_map[val])
        #print(t)
        val=int(sum([pow(2,j) for j in t]))
        bit_map1[i]=val;#np.uint64(val);
    return bit_map1



