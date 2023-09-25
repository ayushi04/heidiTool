
import numpy as np

from app.models import HeidiMatrix
from app.mod_dim.helper.readDataset import ReadDatasetCls 

#read matrix from db, create heidi matrix
def getHeidiMatrixForSubspaceList(subspaceList, datasetObj):
    #for each subspace in subspaceList, get heidi matrix from db
    #return heidi matrix
    try:
        heidi_matrix = np.zeros(shape=(datasetObj.getRow(),datasetObj.getRow()),dtype=np.uint64)
        factor = 1
        for subspace in subspaceList:
            matrix = getHeidiMatrixForSubspace(subspace, datasetObj)
            if matrix is False:
                print('failed to get heidi matrix for subspace', subspace)
            else:
                heidi_matrix=heidi_matrix + matrix*factor
            factor = factor*2
        return heidi_matrix
    except Exception as e:
        print(e)
        print('failed to get heidi matrix for subspace')
        return False
    
# return heidi matrix for input subspace
def getHeidiMatrixForSubspace(subspace, datasetObj):
    try:
        heidi_matrix = np.zeros(shape=(datasetObj.getRow(),datasetObj.getRow()),dtype=np.uint64)    
        matrix = HeidiMatrix.query.filter(HeidiMatrix.dataset == datasetObj.datapath, HeidiMatrix.subspace == subspace).all()
        for row in matrix:
            heidi_matrix[row.row_index][row.col_index] = row.value
        print('got heidi matrix for subspace')
        return heidi_matrix
    except Exception as e:
        print(e)
        print('failed to get heidi matrix for subspace')
        return False    
                            
            
        
    