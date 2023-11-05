import pandas as pd
import app.heidi.order.orderPoints as op
import app.heidi.dataset.api as ds
from app.utils.decorators import TimingDecorator

@TimingDecorator
def orderDataset(datasetPath, orderingDimensions, orderingAlgorithm):
    datasetObj = ds.readDataset(datasetPath)
    data = datasetObj.getInputData()
    filtered_data = data.loc[:,orderingDimensions + ['classLabel']]
    sorted_data = op.order(filtered_data, orderingAlgorithm = "mst_distance")
    return sorted_data

@TimingDecorator
def getSortedOrder(datasetPath, orderingDimensions, orderingAlgorithm = "mst_distance"):
    datasetObj = ds.readDataset(datasetPath)
    data = datasetObj.getInputData()
    originalOrder = list(data.index)
    filtered_data = data.loc[:,orderingDimensions + ['classLabel']]
    sorted_data = op.order(filtered_data, orderingAlgorithm)
    sorted_order = list(sorted_data.index)
    # sort_map = {str(index[i]): sorted_index[i] for i in range(len(index))}
    return originalOrder, sorted_order