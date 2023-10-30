
import app.heidi.database.api as db
import app.heidi.subspace.api as sb
import app.heidi.dataset.api as ds
import app.heidi.matrix.api as mx
import app.heidi.order.api as op

def createAndSaveMatrixToDB(datasetPath, knn=10):
    datasetObj = ds.readDataset(datasetPath)

    #1. Get list of all possible subspaces
    all_subspace = sb.getAllSubspaces(datasetObj.getNumberOfCols())
    print("All possible subspaces are: ", all_subspace)
    
    #2. For each subspace, create matrix and legend
    heidi_matrix_map = mx.createMatrix(datasetObj, all_subspace, knn)
    
    #Get subspace map, key is subspace bit vector (String) and value is list of dimensions in that subspace
    legend = mx.createLegend(datasetObj)
    print('matrix and legend created suuccesfully')
    
    #3. Save matrix and legend to db
    db.saveLegendToDB(legend, datasetObj)
    
    db.saveMatrixToDB(heidi_matrix_map, datasetPath)
    print('matrix and legend saved to database')
    
    
def getImage(datasetPath, selectedDimensions, orderingDimensions, orderingAlgorithm):
    subspaceList = [selectedDimensions]
    matrix_map = db.getHeidiMatrixForSubspaceList([selectedDimensions], datasetPath) # returns :- {('sl', 'sw'): array([[1, 0, 0, ..., 0, 0, 0],
    bitvector_map = db.getBitVectorMap(datasetPath, subspaceList) # returns :- {('sl', 'sw'): 3}
    
    
    # #CODE TO SORT DATASET
    # sorted_data = op.orderDataset(datasetPath, orderingDimensions, orderingAlgorithm)    
    # print('sorted data is \n', sorted_data)
    # print('Data sorted successfully')    
    
    #CODE TO ORDER MATRIX BASED ON SORTED DATA
    original_order, new_order = op.getNewOrder(datasetPath, orderingDimensions, orderingAlgorithm)
    matrix_map = mx.orderMatrix(matrix_map, new_order, original_order)
    
        
    legend = db.getLegend(datasetPath) 
    
    print('\t Legend fetched from database', legend)
    #  Above returns
    # Legend fetched from database                      dataset  subspace        dimensions            color
    # 0   static/uploads/iris2.csv         1              [sl]    [51, 98, 107] 
    # 1   static/uploads/iris2.csv         2              [sw]    [240, 74, 28] 
    
    # bitVector = bitvector_map[tuple(selectedDimensions)]
    
    image_map = mx.createImage(matrix_map, legend)
    
    print('CREATED IMAGE MAP')
    
    consolidated_image = mx.consolidateImage(image_map)
    
    return consolidated_image
    # return matrix_map[tuple(subspaceList)]



    
    
    