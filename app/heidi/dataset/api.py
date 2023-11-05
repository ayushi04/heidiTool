


from app.heidi.dataset.readDataset import ReadDatasetCls
from app.utils.decorators import TimingDecorator

@TimingDecorator
def readDataset(datasetPath):
    datasetObj = ReadDatasetCls()
    datasetObj.readDataset(datasetPath)
    return datasetObj