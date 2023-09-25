import pandas as pd
import numpy as np
from app.mod_dim.helper.common import getAllSubspaces, getSubspaceListFromBitVector
from sklearn.neighbors import NearestNeighbors
from app.mod_dim.fetch import save_matrix_to_db, remove_all_rows_with_dataset, save_dataset_to_db
from app.mod_dim.helper.readDataset import ReadDatasetCls

#CODE TO CREATE HEIDI MATRIX FROM INPUT SUBSPACE AND KNN and save to database
def saveMatrixToDBForSubspace(datasetObj, subspace, knn):
    row = datasetObj.getRow()
    col = datasetObj.getCol()
    data = datasetObj.getFeatureVector()
    
    #create a matrix of size row, row where row is the number of rows in the dataset
    heidi_matrix = np.zeros(shape=(row,row),dtype=np.uint64)
    
    subspace_col = getSubspaceListFromBitVector(subspace, col)
    
    #TODO:- sort data
    
    data=data.iloc[:,subspace_col]
    np_data=data.values
    
    #create knn matrix of input data in input subspace
    nbrs=NearestNeighbors(n_neighbors=knn,algorithm='ball_tree').fit(np_data)
    heidi_matrix=nbrs.kneighbors_graph(np_data).toarray()
    heidi_matrix=heidi_matrix.astype(np.uint64)
    
    save_matrix_to_db(heidi_matrix, subspace, datasetObj.datapath)
    print("Matrix saved for subspace: ", subspace, " and dataset: ", datasetObj, " with subspace: ", subspace)
    return True


def saveMatrixToDB(datasetObj, knn = 10):
    # If the dataset is already present in the db, remove all rows with that dataset
    remove_all_rows_with_dataset(datasetObj.getDatasetPath())
    
    # Get list of all possible subspaces
    all_subspace = getAllSubspaces(datasetObj.getCol())
    print("All possible subspaces are: ", all_subspace)
    
    # For each subspace, save the matrix to the db.
    for subspace in all_subspace:
        saveMatrixToDBForSubspace(datasetObj, subspace, knn)
    
    # Print that the matrix is saved for all subspaces.
    print("Matrix saved for all subspaces")


def readDataset(datasetPath):
    #CODE TO READ DATASET
    robj=ReadDatasetCls()
    robj.readDataset(datasetPath)
    # robj.printDatasetInfo()
    return robj

if __name__ == '__main__':
    print('This is the main function')
    datasetPath='/Users/ayushigupta/Desktop/iris2.csv'
    robj = readDataset(datasetPath)
    robj.printDatasetInfo()
    all_subspaces = getAllSubspaces(robj.col)
    remove_all_rows_with_dataset(datasetPath)
    saveMatrixToDB(robj.data, datasetPath, 10)
    print(all_subspaces)
    # print(data)