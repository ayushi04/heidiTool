
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
    allSubspacesList = sb.getAllSubspacesFromSelectedDimensionSet(selectedDimensions)
    print('allSubspaces are : %s for input selected dimesions : %s' %(allSubspacesList, selectedDimensions))
    
    matrix_map = db.getHeidiMatrixForSubspaceList(allSubspacesList, datasetPath) # returns :- {('sl', 'sw'): array([[1, 0, 0, ..., 0, 0, 0],
    bitvector_map = db.getBitVectorMap(datasetPath, allSubspacesList) # returns :- {('sl', 'sw'): 3}
    
    
    # #CODE TO SORT DATASET
    # sorted_data = op.orderDataset(datasetPath, orderingDimensions, orderingAlgorithm)    
    # print('sorted data is \n', sorted_data)
    # print('Data sorted successfully')    
    
    #CODE TO ORDER MATRIX BASED ON SORTED DATA
    original_order, new_order = op.getSortedOrder(datasetPath, orderingDimensions, orderingAlgorithm)
    matrix_map = mx.orderMatrix(matrix_map, new_order, original_order)
    
    legend = db.getLegend(datasetPath) 
    
    legend = mx.filterLegend(legend, allSubspacesList)
    
    del legend['dataset']   
    
    print('\t Legend fetched from database\n', legend)
    #  Above returns
    # Legend fetched from database                      dataset  subspace        dimensions            color
    # 0   static/uploads/iris2.csv         1              [sl]    [51, 98, 107] 
    # 1   static/uploads/iris2.csv         2              [sw]    [240, 74, 28] 
    
    # bitVector = bitvector_map[tuple(selectedDimensions)]
    
    image_map = mx.createImage(matrix_map, legend)
    
    print('CREATED IMAGE MAP')
    
    final_image = mx.stackAllImages(image_map)
    
    return final_image, legend, new_order, matrix_map
    # return matrix_map[tuple(subspaceList)]

def getConsolidatedImage(datasetPath, selectedDimensions, orderingAlgorithm):
    allSubspacesList = sb.getAllSubspacesFromSelectedDimensionSet(selectedDimensions)
    print('allSubspaces are : %s for input selected dimesions : %s' %(allSubspacesList, selectedDimensions))
    
    matrix_map = db.getHeidiMatrixForSubspaceList(allSubspacesList, datasetPath) # returns :- {('sl', 'sw'): array([[1, 0, 0, ..., 0, 0, 0],
    
    sorted_matrix_map = {}
    new_order_map = {}
    for subspace in matrix_map:
        orderingDimensions = list(subspace)
        original_order, new_order = op.getSortedOrder(datasetPath, orderingDimensions, orderingAlgorithm)
        updated_matrix = mx.orderMatrix({subspace: matrix_map[subspace]}, new_order, original_order)
        sorted_matrix_map[subspace] = updated_matrix[subspace]
        new_order_map[subspace] = new_order
    legend = db.getLegend(datasetPath) 
    legend = mx.filterLegend(legend, allSubspacesList)
    del legend['dataset']   
    image_map = mx.createImage(sorted_matrix_map, legend)
    final_image = mx.stackAllImages(image_map)
    # final_image.save('static/output_image.png')
    return final_image, legend, new_order_map, matrix_map


def getPoints(datasetPath, matrixMap, rowPoint, colPoint):
    # datasetObj = ds.readDataset(datasetPath)
    rowPoint = int(rowPoint)
    colPoint = int(colPoint)
    subspaceList = mx.getSelectedPixel_subspaces(matrixMap, rowPoint, colPoint)
    print('Subspace of pixel clicked:', subspaceList)
    row_cluster, col_cluster = ds.getSelectedPixel_clusterId(rowPoint, colPoint, datasetPath)
    print('Row cluster : ({}), Col cluster : ({})'.format(row_cluster, col_cluster))
    bitvector_map = db.getBitVectorMap(datasetPath, subspaceList) # returns :- {('sl', 'sw'): 3}
    allPoints = {}
    for subspace in subspaceList:
        subspace_bit_vector = bitvector_map[subspace]
        df = db.getAllPointsInCluster(datasetPath, subspace_bit_vector, row_cluster, col_cluster)
        allPoints[subspace] = df
    return allPoints

def createLegend(datasetPath):
    """
    Create a legend for the given dataset object.
    Args:
        datasetObj: The dataset object for which the legend is to be created.
    Returns:
        The created legend object.
    """
    datasetObj = ds.readDataset(datasetPath)
    return mx.createLegend(datasetObj)




    
    
    