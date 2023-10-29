from app.heidi.matrix import constants
from app.heidi.subspace.api import getAllSubspaces, getColumnNameListFromBitVector


def createLegend(datasetObj):
    legend = {}
    all_subspaces = getAllSubspaces(datasetObj.getNumberOfCols())
    color_map = createColorMap(all_subspaces)
    try:
        for subspace in all_subspaces:
            # subspace_col = getColumnIndexListFromBitVector(subspace, datasetObj.getNumberOfCols())
            column_names = getColumnNameListFromBitVector(subspace, datasetObj.getNumberOfCols(), datasetObj.getColumNames())
            legend[subspace] = tuple([column_names, color_map[subspace]])
        print('Legend created for dataset: ', datasetObj.getDatasetPath())
        print('Legend created is: ' )
        #display legend map
        for key, value in legend.items():
            print(key, ' : ', value[0], ' : ', value[1])
        print('----------------------------------------------------------------')
    except Exception as e:
        print('Error in creating legend for dataset: ', datasetObj.getDatasetPath())
        print(e)
    return legend

def createColorMap(subspaceList):
    colorMap = {}
    color = constants.CLUSTER_COLORS
    i = 0
    for subspace in subspaceList:
        colorMap[subspace] = color[i]
        i += 1
    return colorMap