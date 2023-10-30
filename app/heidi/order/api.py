import pandas as pd
import app.heidi.order.orderPoints as op
import app.heidi.dataset.api as ds

def orderDataset(datasetPath, orderingDimensions, orderingAlgorithm):
    datasetObj = ds.readDataset(datasetPath)
    data = datasetObj.getInputData()
    filtered_data = data.loc[:,orderingDimensions + ['classLabel']]
    sorted_data = op.order(filtered_data, orderingAlgorithm = "mst_distance")
    return sorted_data

def getNewOrder(datasetPath, orderingDimensions, orderingAlgorithm):
    datasetObj = ds.readDataset(datasetPath)
    data = datasetObj.getInputData()
    index = list(data.index)
    filtered_data = data.loc[:,orderingDimensions + ['classLabel']]
    sorted_data = op.order(filtered_data, orderingAlgorithm = "mst_distance")
    sorted_index = list(sorted_data.index)
    # sort_map = {str(index[i]): sorted_index[i] for i in range(len(index))}
    return index, sorted_index