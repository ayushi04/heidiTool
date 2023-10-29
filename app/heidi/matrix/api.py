import app.heidi.matrix.legend as legend
import app.heidi.matrix.matrix as matrix
import app.heidi.matrix.image as image

def createLegend(datasetObj):
    return legend.createLegend(datasetObj)

def createMatrix(datasetObj, all_subspace, knn = 10) :
    return matrix.createMatrix(datasetObj, all_subspace, knn)

def createMatrixForSubspace(datasetObj, subspace, knn = 10) :
    return matrix.createMatrixForSubspace(datasetObj, subspace, knn)

def createImage(matrix_map, legend):
    return image.createImage(matrix_map, legend)

def consolidateImage(image_map):
    return image.consolidateImage(image_map)