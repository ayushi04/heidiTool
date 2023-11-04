
import numpy as np
from app.heidi.database.database import get_bit_vector_for_subspace
from app.heidi.dataset import readDataset
from app.heidi.subspace.api import getAllSubspaces
from app.heidi.database.database import *
from app.custom_exceptions import MyCustomException

#read matrix from db, create heidi matrix
def getHeidiMatrixForBitVectorsList(bitVectorList, datasetObj):
    #for each subspace in subspaceList, get heidi matrix from db
    #return heidi matrix
    try:
        heidi_matrix = np.zeros(shape=(datasetObj.getRow(),datasetObj.getRow()),dtype=np.uint64)
        factor = 1
        matrix_map = {}
        for bitVector in bitVectorList:
            # print('-------BitVector: ', bitVector, '-------')
            matrix = get_matrix_from_db_for_bit_vector(datasetObj.getDatasetPath(), datasetObj.getRow(), bitVector)
            if matrix is False:
                print('Failed to get heidi matrix for subspace', bitVector)
            else:
                heidi_matrix=heidi_matrix + matrix*factor
                matrix_map[bitVector] = matrix
            factor = factor*2
        return matrix_map
    except Exception as e:
        print(e)
        print('Failed to get heidi matrix for subspace')
        raise MyCustomException('failed to get matrix from db for bitVectorList : %s and dataset : %s' %(bitVectorList, datasetObj.getDatasetPath()))

# checked
def getHeidiMatrixForSubspaceList(subspaceList, datasetObj):
    bit_vectors = getBitVector(datasetObj.getDatasetPath(), subspaceList)
    
    print('Bit vectors list : %s , for input subspaceList : %s fetched from database is' %(bit_vectors, subspaceList))
    matrix_map = getHeidiMatrixForBitVectorsList(bit_vectors, datasetObj)
    subspace_matrix_map = {}
    for i in range(0,len(bit_vectors)):
        subspace = subspaceList[i]
        bit_vector = bit_vectors[i]
        print('Subspace : %s , bit vector : %s' %(subspace, bit_vector))
        subspace_matrix_map[tuple(subspace)]=matrix_map[bit_vector]
        
    print('heidi matrix for subset of dimensions', subspaceList, 'fetched from database')
    return subspace_matrix_map    
    
# checked
def getBitVector(datasetPath, subspaceList):
    bit_vectors = []
    for subspace in subspaceList:
        bit_vector = get_bit_vector_for_subspace(datasetPath, subspace)
        bit_vectors = bit_vectors + [int(bit_vector)]
    return bit_vectors

def getBitVectorMap(datasetPath, subspaceList):
    # print('getBitVectorMap Input : ', datasetPath, subspaceList)
    bit_vector_map = {}
    for subspace in subspaceList:
        bit_vector = get_bit_vector_for_subspace(datasetPath, subspace)
        bit_vector_map[tuple(subspace)] = int(bit_vector)
    return bit_vector_map

def getColumns(datasetPath):
    return get_columns(datasetPath)

def getLegend(datasetPath):
    return get_legend(datasetPath)

def getMatrix(datasetPath, knn):
    datasetObj = readDataset(datasetPath)
    datasetObj.printDatasetInfo()
    all_subspaces = getAllSubspaces(datasetObj.col)
    return getHeidiMatrixForSubspaceList(all_subspaces, datasetObj)
    return get_matrix_from_db_for_bit_vector(datasetObj.getDatasetPath(), datasetObj.getRow(), all_subspaces)
    
    