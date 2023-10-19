
import numpy as np

from app.mod_dim.helper.readDataset import ReadDatasetCls 
from app.heidi.database import *

#read matrix from db, create heidi matrix
def getHeidiMatrixForListOfBitVectors(subspaceList, datasetObj):
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


def getHeidiMatrixForListofSubsetofDimensions(listOfSubsetofDimensions, datasetObj):
    bit_vectors = []
    for subsetofDimensions in listOfSubsetofDimensions:
        bit_vector = getBitVectorFromColumnNameList(datasetObj.getDatasetPath(), subsetofDimensions)
        bit_vectors = bit_vectors + [bit_vector]
    
    print('bit vectors for subset of dimensions', listOfSubsetofDimensions, 'fetched from database is', bit_vectors)    
    heidi_matrix = getHeidiMatrixForListOfBitVectors(bit_vectors, datasetObj)
    print('heidi matrix for subset of dimensions', listOfSubsetofDimensions, 'fetched from database')
    return heidi_matrix    
    
# return heidi matrix for input subspace
def getHeidiMatrixForSubspace(subspace, datasetObj):
    get_matrix_from_db_for_subspace(subspace, datasetObj)

def getBitVectorFromColumnNameList(datasetPath, column_name_list):
    return get_bitvector_from_column_name_list(datasetPath, column_name_list)

def getColumns(datasetPath):
    return get_columns(datasetPath)
    
    