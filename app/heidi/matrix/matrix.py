import pandas as pd
import numpy as np
from app.heidi.subspace.api import getColumnIndexListFromBitVector
from app.heidi.subspace.api import getColumnNameListFromBitVector
from sklearn.neighbors import NearestNeighbors
from heidi.database.database import *


# Method to create Heidi Matrix for all subspaces
def createMatrix(datasetObj, all_subspace, knn = 10) :
    
    print('----------------------------------------------------------------')
    #Get subspace map, key is subspace bit vector (String) and value is list of dimensions in that subspace
    all_matrix = {}
    # For each subspace, save the matrix to the db.
    for subspace in all_subspace:
        matrix = createMatrixForSubspace(datasetObj, subspace, knn)
        all_matrix[subspace] = matrix
    return all_matrix


# Method to create Heidi Matrix for a given subspace
# INPUT: datasetObj, subspace= 10, knn=10
# OUTPUT: N X N matrix where N is the number of rows in the dataset
def createMatrixForSubspace(datasetObj, subspace, knn = 10) :
    row = datasetObj.getRow()
    col = datasetObj.getNumberOfCols()
    data = datasetObj.getFeatureVector()
    
    #create a matrix of size row, row where row is the number of rows in the dataset
    heidi_matrix = np.zeros(shape=(row,row),dtype=np.uint64)
    subspace_col = getColumnIndexListFromBitVector(subspace, col)
    column_names = getColumnNameListFromBitVector(subspace, datasetObj.getNumberOfCols(), datasetObj.getColumNames())
    print(" %s (%s) : '%s'" %(column_names, subspace_col,subspace))
    
    #TODO:- sort data
    
    data=data.iloc[:,subspace_col]
    np_data=data.values
    
    #create knn matrix of input data in input subspace
    nbrs=NearestNeighbors(n_neighbors=knn,algorithm='ball_tree').fit(np_data)
    heidi_matrix=nbrs.kneighbors_graph(np_data).toarray()
    heidi_matrix=heidi_matrix.astype(np.uint64)
    return heidi_matrix

def orderMatrix(matrix_map, new_order, original_order):
    new_matrix_map = {}
    original_order_dict = {name: index for index, name in enumerate(original_order)}
    reshuttle_index = [original_order_dict[value] for value in new_order]
    for subspace, matrix in matrix_map.items():
        # rows = [original_order_dict[value] for value in new_order]
        # cols = [original_order_dict[value] for value in new_order]
        new_matrix = matrix[np.ix_(reshuttle_index, reshuttle_index)]
        new_matrix_map[subspace] = new_matrix

    return new_matrix_map

def getSelectedPixel_subspaces(matrix_map, rowPoint, colPoint):
    selectedPixel_subspaces = []
    for subspace, matrix in matrix_map.items():
        print(matrix.shape)
        if matrix[rowPoint][colPoint] == 1:
            selectedPixel_subspaces.append(subspace)
    return selectedPixel_subspaces

    