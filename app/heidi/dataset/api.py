


import json
from app.heidi.dataset.readDataset import ReadDatasetCls
from app.utils.decorators import TimingDecorator

@TimingDecorator
def readDataset(datasetPath):
    datasetObj = ReadDatasetCls()
    datasetObj.readDataset(datasetPath)
    return datasetObj

@TimingDecorator
def getPointId(datapath,index):
    datasetObj = ReadDatasetCls()
    return datasetObj.inputData.index[index]

@TimingDecorator
def getSelectedPixel_clusterId(rowPoint, colPoint, datasetPath):
    datasetObj = ReadDatasetCls()
    datasetObj.readDataset(datasetPath)
    rowPoint = datasetObj.inputData.index[rowPoint]
    colPoint = datasetObj.inputData.index[colPoint]
    row_cluster = datasetObj.getInputData().loc[rowPoint]['classLabel']
    col_cluster = datasetObj.getInputData().loc[colPoint]['classLabel']
    return row_cluster, col_cluster

def getPointValue(datasetPath, subspace, rowPoint):
    datasetObj = ReadDatasetCls()
    datasetObj.readDataset(datasetPath)
    rowPoint = datasetObj.inputData.loc[rowPoint,:]
    if subspace:
        rowPoint = rowPoint[list(subspace)]
    return rowPoint.to_dict()
