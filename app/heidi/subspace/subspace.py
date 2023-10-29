
from itertools import combinations
import math


def getColumnIndexListFromBitVector(bitVector, col):
    frmt=str(col)+'b'
    bin_value=str(format(bitVector,frmt))
    bin_value=bin_value[::-1]
    if len(bin_value)>col:
        print("error: subspace value(%s) is greater than the number of columns (%s) in the dataset" %(bitVector,col))
        return False
    subspace_col=[index for index,value in enumerate(bin_value) if value=='1']
    return subspace_col


def getAllSubspaces(dims):
    #the maximum number of subspaces is 2^dims
    max_count=int(math.pow(2,dims))
    #create a list of all subspaces, from 1 to max_count
    allsubspaces=range(1,max_count)
    #sort the subspaces by the number of 1's in their binary representation
    allsubspaces=sorted(allsubspaces,key=lambda x:sum(int(d)for d in bin(x)[2:]))
    return allsubspaces


def getColumnNameListFromBitVector(bitVector, col, all_col_names):
    subspace_indexes = getColumnIndexListFromBitVector(bitVector, col)
    filtered_column_names = [all_col_names[i] for i in subspace_indexes]
    return filtered_column_names


def subsets(s):
    t=[]
    for cardinality in range(len(s) + 1):
        #yield from combinations(s, cardinality)  #IMPORTANT : this line i changed to drop down to python2 because there was giving error in python2
        for i in combinations(s, cardinality): # this for loop because of python2, thus use either yield line or this loop, with yield no need to return
            t=t+[i]
    return t