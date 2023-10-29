


from app.heidi.dataset.readDataset import ReadDatasetCls

def readDataset(datasetPath):
    datasetObj = ReadDatasetCls()
    datasetObj.readDataset(datasetPath)
    return datasetObj