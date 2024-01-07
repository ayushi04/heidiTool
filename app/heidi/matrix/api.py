import app.heidi.matrix.legend as legend
import app.heidi.matrix.matrix as matrix
import app.heidi.matrix.image as image
from app.utils.decorators import TimingDecorator


@TimingDecorator
def createLegend(datasetObj):
    return legend.createLegend(datasetObj)

@TimingDecorator
def createMatrix(datasetObj, all_subspace, knn = 10) :
    return matrix.createMatrix(datasetObj, all_subspace, knn)

@TimingDecorator
def createMatrixForSubspace(datasetObj, subspace, knn = 10) :
    return matrix.createMatrixForSubspace(datasetObj, subspace, knn)

@TimingDecorator
def createImage(matrix_map, legend):
    return image.createImage(matrix_map, legend)

@TimingDecorator
def stackAllImages(image_map):
    return image.stackAllImages(image_map)

@TimingDecorator
def orderMatrix(matrix_map, new_order, original_order):
    return matrix.orderMatrix(matrix_map, new_order, original_order)

@TimingDecorator
def filterLegend(legend_df, subspaceList):
    return legend.filterLegend(legend_df, subspaceList)

def getSelectedPixel_subspaces(matrix_map, rowPoint, colPoint):
    return matrix.getSelectedPixel_subspaces(matrix_map, rowPoint, colPoint)

