import math



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


