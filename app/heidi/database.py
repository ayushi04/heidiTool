#In this file we will do all db related operations
#like saving matrix to db, removing all rows with dataset, getting heidi matrix for subspace
#and saving dataset to db

from app import db
import numpy as np
from app.custom_exceptions import MyCustomException
from models import HeidiMatrix, Dataset, Legend

#CODE TO GET MATRIX FROM DB
def get_matrix_from_db_for_subspace(datasetObj, subspace):
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
    
def get_bitvector_from_column_name_list(datapath, column_name_list):
    try:
        print('Input column name list is ', column_name_list, 'datapath is ', datapath)
        print( Legend.query.filter((Legend.dataset == datapath) &  (Legend.dimensions == str(column_name_list))))
        legend = Legend.query.filter((Legend.dataset == datapath) &  (Legend.subspace == 4)).first()
        if legend is None:
            print('no legend found for dataset %s and dimensions %s' %(datapath, column_name_list))
            return False
        subspace = legend.subspace
        print('got subspace(%s) from legend ' %(subspace))
        return subspace
    except Exception as e:
        print(e)
        print('failed to get subspace from legend')
        return False
        

#CODE TO SAVE MATRIX TO DB
def save_matrix_to_db(heidi_matrix,subspace, dataset):
    #for input matrix, get all tuple of row and column points, and their corresponding values
    #save these tuples, subspace and value to db where value is non-zero
    try:
        for i, row in enumerate(heidi_matrix):
            for j, value in enumerate(row):
                if value != 0:
                    # Insert the data into the table
                    db.session.add(HeidiMatrix(subspace=subspace, row_index=i, col_index=j, dataset=dataset, value=value))
        db.session.commit()
        print('saved matrix to db')
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

def get_heidi_matrix_for_subspace(dataset, subspace):
    try:
        heidi_matrix = HeidiMatrix.query.filter(HeidiMatrix.dataset == dataset, HeidiMatrix.subspace == subspace).all()
        print('got heidi matrix for subspace')
    except Exception as e:
        print(e)
        db.session.rollback()
        print('failed to get heidi matrix for subspace')
        return False
    return heidi_matrix

def save_dataset_to_db(datasetObj):
    rows = datasetObj.getRow()
    cols = datasetObj.getCol()
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
            db.session.add(Legend(dataset=datasetName, subspace = key, dimensions = value))
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

        
        
    
        
    
    

    
    




        
                
    
    

