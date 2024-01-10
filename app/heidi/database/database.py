#In this file we will do all db related operations
#like saving matrix to db, removing all rows with dataset, getting heidi matrix for subspace
#and saving dataset to db

import json
import ast
import pandas as pd
from app import db
import numpy as np
from custom_exceptions import MyCustomException
from models import HeidiMatrix, Dataset, Legend


def get_legend(datasetPath):
    try:
        legend = Legend.query.filter(Legend.dataset == datasetPath).all()
        legend_data = [
            {'dataset': item.dataset, 'subspace': item.subspace,
             'dimensions': json.loads(item.dimensions), 'color': json.loads(item.color)}
            for item in legend
        ]
        df = pd.DataFrame(legend_data)
        # df['color'] = [list(i) for i in df['color']]
        # df['dimensions'] = [list(i) for i in df['dimensions']]
        print('got legend from db')
        return df
    except Exception as e:
        print(e)
        print('failed to get legend from db')
        return False
    
    
#CODE TO GET MATRIX FROM DB
def get_matrix_from_db_for_bit_vector(datapath, row, subspace):
    heidi_matrix = np.zeros(shape=(row, row),dtype=np.uint64)    
    print('Input of get_matrix_from_db_for_subspace is ', datapath, 'and subspace is ', subspace )
    try:
        matrix = HeidiMatrix.query.filter(HeidiMatrix.dataset == datapath, HeidiMatrix.subspace == subspace).all()
        for row in matrix:
            heidi_matrix[row.row_index][row.col_index] = int(row.value)
        # print('Created heidi matrix for subspace')
        return heidi_matrix
    except Exception as e:
        print(e)
        print('failed to get heidi matrix for subspace')
        return False    
    
# checked
# Subspace is - column name list
# Data fetched from Table - Legend
# not to be called outside this file
# checked
def get_bit_vector_for_subspace(datapath, subspace):
    try:
        # print('Input column name list is ', subspace, 'datapath is ', datapath)
        # column_name_string = ', '.join(column_name_list)
        column_name_string = json.dumps(subspace)
        # print( Legend.query.filter((Legend.dataset == datapath) &  (Legend.dimensions == column_name_string)))
        legend = Legend.query.filter((Legend.dataset == datapath) &  (Legend.dimensions == column_name_string)).first()
        if legend is None:
            print('no legend found for dataset %s and dimensions %s' %(datapath, column_name_string))
            return False
        bitVector = legend.subspace
        # print('Fetched bitvector(%s) from database (legend table) for subspace(%s)' %(bitVector, column_name_string))
        return bitVector
    except Exception as e:
        print(e)
        print('Failed to get bitvector from legend for subspace(%s)' %(column_name_string))
        raise MyCustomException('Failed to get bitvector from legend for subspace: %s' %(column_name_string))
      
# checked
"""        
CODE TO SAVE MATRIX TO DB
Input:- 
subspace - 7 
matrix - [[1 0 0 ... 0 0 0]
 [0 1 1 ... 0 0 0]
 [0 0 1 ... 0 0 0]
 ...
 [0 0 0 ... 1 0 0]
 [0 0 0 ... 1 1 1]
 [0 0 0 ... 0 0 1]]
"""
def save_matrix_to_db(heidi_matrix,subspace, datasetObj):
    dataset = datasetObj.getDatasetPath()
    #for input matrix, get all tuple of row and column points, and their corresponding values
    #save these tuples, subspace and value to db where value is non-zero
    try:
        for i, row in enumerate(heidi_matrix):
            for j, value in enumerate(row):
                if value != 0:
                    # Insert the data into the table
                    # print(datasetObj.getClusterId(i), datasetObj.getClusterId(j))
                    db.session.add(HeidiMatrix(subspace=subspace, row_index=i, col_index=j, row_point=datasetObj.getPointId(i), col_point=datasetObj.getPointId(j), row_cluster = datasetObj.getClusterId(i), col_cluster = datasetObj.getClusterId(j), dataset=dataset, value=int(value)))
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        print('failed to save matrix to db')
        raise MyCustomException('failed to save matrix to db for subspace : %s and dataset : %s' %(subspace, dataset))
    return True

def get_columns(dataset):
    try:
        datasetObj = Dataset.query.filter(Dataset.dataset == dataset).first()
        if datasetObj is None:
            print('no dataset found with name %s' %(dataset))
            return False
        return datasetObj.get_column_names_list()
    except Exception as e:
        print(e)
        print('failed to get columns for dataset %s' %(dataset))
        return False


def remove_all_rows_with_dataset(dataset):
    #for each row in heidi_matrix, remove all rows with dataset=dataset
    try:
        HeidiMatrix.query.filter(HeidiMatrix.dataset == dataset).delete()
        db.session.commit()
        print('removed all rows with dataset')
    except Exception as e:
        print(e)
        db.session.rollback()
        print('failed to remove all rows with dataset')
        raise MyCustomException('failed to remove all rows with dataset(%s)' %(dataset))
    return True

# def get_heidi_matrix_for_subspace(dataset, subspace):
#     try:
#         heidi_matrix = HeidiMatrix.query.filter(HeidiMatrix.dataset == dataset, HeidiMatrix.subspace == subspace).all()
#         print('got heidi matrix for subspace')
#     except Exception as e:
#         print(e)
#         db.session.rollback()
#         print('failed to get heidi matrix for subspace')
#         return False
#     return heidi_matrix

def save_dataset_to_db(datasetObj):
    rows = datasetObj.getRow()
    cols = datasetObj.getNumberOfCols()
    try:
        # add new dataset to db
        db.session.add(Dataset(dataset=datasetObj.getDatasetPath(), no_of_rows=rows, no_of_cols=cols, column_names_list = datasetObj.getColumNames()))
        db.session.commit()
        print('saved dataset to db')
    except Exception as e:
        print(e)
        db.session.rollback()
        print('failed to save dataset to db')
        raise MyCustomException('failed to save dataset to db')
    return True

def delete_dataset_from_db(datasetName):
    try:
        Dataset.query.filter(Dataset.dataset == datasetName).delete()
        db.session.commit()
        print('removed %s from Dataset Table ' %(datasetName))
    except Exception as e:
        print(e)
        db.session.rollback()
        print('failed to remove %s from Dataset Table ' %(datasetName))
        raise MyCustomException('failed to remove %s from Dataset Table ' %(datasetName))
    return True

def save_legend_to_db(legend, datasetObj):
    datasetName = datasetObj.getDatasetPath()
    try:
        for key, value in legend.items():
            # value ', '.join(value)
            # print('Key is %s and value is %s, %s' %(key, value[0], value[1]))
            db.session.add(Legend(dataset=datasetName, subspace = key, dimensions = value[0], color = value[1]))
        db.session.commit()
        print('saved legend to db')
    except Exception as e:
        print(e)
        db.session.rollback()
        print('failed to save legend to db')
        print('Legend input is : %s' %(legend))
        raise MyCustomException('failed to save legend to db')
    return True

def delete_legend_from_db(datasetObj):
    datasetName = datasetObj.getDatasetPath()
    try:
        Legend.query.filter(Legend.dataset == datasetName).delete()
        db.session.commit()
        print('removed %s from Legend Table ' %(datasetName))
    except Exception as e:
        print(e)
        db.session.rollback()
        print('failed to remove %s from Legend Table ' %(datasetName))
        raise MyCustomException('failed to remove %s from Legend Table ' %(datasetName))
    return True

def getAllPointsInClusterFromDB(datasetPath, row_cluster, col_cluster, subspace = None):
    try:
        print('DB Op: method: getAllPointsInClusterFromDB: Input : datasetPath : {}, row_cluster : {}, col_cluster : {}, subspace : {}'.format(datasetPath, row_cluster, col_cluster, subspace))
        points = []
        if subspace is None:
            points = HeidiMatrix.query.filter(HeidiMatrix.dataset == datasetPath, HeidiMatrix.row_cluster == row_cluster, HeidiMatrix.col_cluster == col_cluster).all()
        else:
            #check if subspace is string make it list of string
            if isinstance(subspace, str):
                subspace = [subspace]
            points = HeidiMatrix.query.filter(HeidiMatrix.dataset == datasetPath, HeidiMatrix.subspace.in_(subspace) , HeidiMatrix.row_cluster == row_cluster, HeidiMatrix.col_cluster == col_cluster).all()
        df = pd.DataFrame([{'row_point': item.row_point, 'col_point': item.col_point, 'subspace': item.subspace} for item in points])
        print('DB Op: {} points fetched from db for input row_cluster : {}, col_cluster : {}, subspace : {}'.format(len(df), row_cluster, col_cluster, subspace))
        return df
    except Exception as e:
        print(e)
        db.session.rollback()
        print('failed to get points in cluster from db')
        return False
    

        
        
    
        
    
    

    
    




        
                
    
    

