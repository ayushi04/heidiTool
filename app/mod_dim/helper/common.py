import math
from itertools import combinations
from app.mod_dim.database import *

def getAllSubspaces(dims):
    #the maximum number of subspaces is 2^dims
    max_count=int(math.pow(2,dims))
    #create a list of all subspaces, from 1 to max_count
    allsubspaces=range(1,max_count)
    #sort the subspaces by the number of 1's in their binary representation
    allsubspaces=sorted(allsubspaces,key=lambda x:sum(int(d)for d in bin(x)[2:]))
    return allsubspaces


def getSubspaceListFromBitVector(subspace, col):
    frmt=str(col)+'b'
    bin_value=str(format(subspace,frmt))
    bin_value=bin_value[::-1]
    if len(bin_value)>col:
        print("error: subspace value(%s) is greater than the number of columns (%s) in the dataset" %(subspace,col))
        return False
    subspace_col=[index for index,value in enumerate(bin_value) if value=='1']
    print ("%s : '%s'" %(subspace_col,bin_value[::-1]))
    return subspace_col

def getColumnNameListFromBitVector(subspace, col, column_names_list):
    subspace_indexes = getSubspaceListFromBitVector(subspace, col)
    filtered_column_names = [column_names_list[i] for i in subspace_indexes]
    return filtered_column_names
    

def subsets(s):
    t=[]
    for cardinality in range(len(s) + 1):
        #yield from combinations(s, cardinality)  #IMPORTANT : this line i changed to drop down to python2 because there was giving error in python2
        for i in combinations(s, cardinality): # this for loop because of python2, thus use either yield line or this loop, with yield no need to return
            t=t+[i]
    return t

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



