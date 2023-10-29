from app.heidi.dataset.api import readDataset
from app.heidi.subspace.api import getAllSubspaces
from heidi.database import fetch
from heidi.database import upload

# method to get legend for input dataset
# RETURN:- dataframe
# Legend fetched from database                      dataset  subspace        dimensions            color
# 0   static/uploads/iris2.csv         1              [sl]    [51, 98, 107] 
# 1   static/uploads/iris2.csv         2              [sw]    [240, 74, 28] 
def getLegend(datasetPath):
    return fetch.getLegend(datasetPath)

# Code to get Heidi Matrix for all subspace
def getHeidiMatrix(datasetPath, knn):
    datasetObj = readDataset(datasetPath)
    all_subspaces = getAllSubspaces(datasetObj.col)
    return fetch.getHeidiMatrixForBitVectorsList(all_subspaces, datasetObj)

# Code to get Heidi Matrix for one input bitVector
def getHeidiMatrixForBitVector(bitVector, datasetObj):
    return fetch.getHeidiMatrixForBitVectorsList([bitVector], datasetObj)

# Code to get Heidi Matrix for input subspace`s` list
# INPUT: 
# subspace = [['sl'],['sl','sw'],['sl','sw','pl'],['sl','sw','pl','pw']]
# datasetPath = 'static/uploads/iris2.csv'
# OUTPUT:
# {('sl', 'sw'): array([[1, 0, 0, ..., 0, 0, 0], .... }
def getHeidiMatrixForSubspaceList(subspaceList, datasetPath):
    datasetObj = readDataset(datasetPath)
    print('dataset read successfully.')
    return fetch.getHeidiMatrixForSubspaceList(subspaceList, datasetObj)


# Code to get bit vector for input subspace List
# INPUT: 
# subspace = [['sl'],['sl','sw'],['sl','sw','pl'],['sl','sw','pl','pw']]
# datasetPath = 'static/uploads/iris2.csv'
# OUTPUT:
# bit_vectors =    ---TBC
# checked 
def getBitVector(subspaceList, datasetPath):
    return fetch.getBitVector(datasetPath, subspaceList)

# INPUT :
# datasetPath : static/uploads/iris2.csv 
# subspaceList : [['sl', 'sw']]
# OUTPUT:
# {('sl', 'sw'): 3}
def getBitVectorMap(datasetPath, subspaceList):
    return fetch.getBitVectorMap(datasetPath, subspaceList)

def getColumns(datasetPath):
    return fetch.getColumns(datasetPath)

# checked
#save matrix to database for all subspaces
def saveMatrixToDB(heidi_matrix_map, datasetPath, knn = 10):
    return upload.saveMatrixToDB(heidi_matrix_map, datasetPath, knn)

# checked
def saveLegendToDB(legend, datasetObj):
    return upload.saveLegendToDB(legend, datasetObj)

# checked
def saveDatasetToDB(datasetPath):
    datasetObj = readDataset(datasetPath)
    return upload.saveDatasetToDB(datasetObj)

