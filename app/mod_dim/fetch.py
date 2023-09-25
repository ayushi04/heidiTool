#In this file we will do all db related operations
#like saving matrix to db, removing all rows with dataset, getting heidi matrix for subspace
#and saving dataset to db

from app import db
from app.custom_exceptions import MyCustomException
from models import HeidiMatrix, Dataset

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
        db.session.add(Dataset(dataset=datasetObj.getDatasetPath(), rows=rows, cols=cols))
        db.session.commit()
        print('saved dataset to db')
    except Exception as e:
        print(e)
        db.session.rollback()
        print('failed to save dataset to db')
        raise MyCustomException('failed to save dataset to db')
    return True

    
    




        
                
    
    

