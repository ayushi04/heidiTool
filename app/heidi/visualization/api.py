
import app.heidi.dataset.api as ds
import app.heidi.visualization.helper as helper

def getSubspaceOverlapSummary(datasetPath, df_matrix):
    datasetObj = ds.readDataset(datasetPath)
    df_dataset = datasetObj.inputData
    df_dataset['id'] = df_dataset.index
    print(df_dataset)
    
    all_bitvectors = list(set(df_matrix['bitvector']))
    rowPointsClassLabel = 0
    columnPointsClassLabel=1
    num_rowPointsClassLabel = len(list(set(df_dataset['id'][df_dataset['classLabel']==rowPointsClassLabel])))
    num_columnPointsClassLabel = len(list(set(df_dataset['id'][df_dataset['classLabel']==columnPointsClassLabel])))
    summary_list=[]
    for bitvector in all_bitvectors[1:]:
        df_subset, subspace = helper.get_dataframe_for_bitvector(df_matrix, df_dataset, bitvector)
        rowPointsId = list(set(df_subset[df_subset['classLabel'] == rowPointsClassLabel]['id']))
        colPointsId = list(set(df_subset[df_subset['classLabel'] == columnPointsClassLabel]['id']))
        summary_list.append({
                "rowPoints": rowPointsId,
                "columnPoints": colPointsId,
                "num_rowPoints": len(rowPointsId),
                "num_colPoints": len(colPointsId),
                "percentage_rowPoints": f"{(len(rowPointsId) / num_rowPointsClassLabel) * 100:.2f}%",
                "percentage_colPoints": f"{(len(colPointsId) / num_columnPointsClassLabel) * 100:.2f}%",
                "subspace": subspace
            })
    
    return summary_list
        
    
    