import pandas as pd
import numpy as np
from app.heidi.matrix.api import createMatrixForSubspace
from app.heidi.subspace.api import getAllSubspaces, getColumnNameListFromBitVector
from sklearn.neighbors import NearestNeighbors
from app.heidi.database.database import *
from app.heidi.dataset.api import readDataset

#CODE TO CREATE HEIDI MATRIX FROM INPUT SUBSPACE AND KNN and save to database
def saveMatrixToDBForSubspace(datasetObj, subspace, knn):
    heidi_matrix = createMatrixForSubspace(datasetObj, subspace, knn)
    
    save_matrix_to_db(heidi_matrix, subspace, datasetObj.datapath)
    print("Matrix saved for subspace: ", subspace, " and dataset: ", datasetObj, " with subspace: ", subspace)
    return True


def saveMatrixToDB(heidi_matrix_map, datasetObj, knn = 10):
    # If the dataset is already present in the db, remove all rows with that dataset
    datasetPath = datasetObj.getDatasetPath()
    remove_all_rows_with_dataset(datasetPath)
    for subspace in heidi_matrix_map:
        matrix = heidi_matrix_map[subspace]
        save_matrix_to_db(matrix, subspace, datasetObj)

    # Print that the matrix is saved for all subspaces.
    print("Matrix saved for all subspaces")
    return True
    
def saveLegendToDB(legend, datasetObj):
    deleteLegendFromDB(datasetObj)
    save_legend_to_db(legend, datasetObj)
    print("Matrix saved to DB")
    
def saveDatasetToDB(datasetObj):
    delete_dataset_from_db(datasetObj.getDatasetPath())
    save_dataset_to_db(datasetObj)

def deleteLegendFromDB(datasetObj):
    delete_legend_from_db(datasetObj)
    
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