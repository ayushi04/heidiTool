import json
from flask import Blueprint, jsonify, request, Response

from app.heidi.dataset.api import readDataset, getPointValue
from app.heidi.database.api import saveMatrixToDB, saveDatasetToDB, getHeidiMatrixForSubspaceList, getColumns
import app.heidi.api as hd

import io
import base64


heidi_controller = Blueprint('heidi', __name__, url_prefix='/heidi')

@heidi_controller.route('/read-dataset', methods=['GET'])
def read_dataset_route():
    dataset_path = request.args.get('dataset_path')  # Get the dataset path from the query parameter
    if not dataset_path:
        return jsonify({"error": "Dataset path is missing"}), 400
    try:
        data = readDataset(dataset_path)
        return jsonify({"data": data.to_dict(orient="records")}), 200
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:  
        return jsonify({"error": str(e)}), 500

@heidi_controller.route('/create-heidi-matrix', methods=['POST'])
def create_heidi_matrix_route():
    # Get the dataset path from the query parameter
    datasetPath = request.args.get('dataset_path')
    if not datasetPath:
        return jsonify({"error": "Dataset path is missing"}), 400
    try:
        robj=readDataset(datasetPath)
        saveDatasetToDB(robj)
        data = saveMatrixToDB(robj)
        return jsonify({"data": data.to_dict(orient="records")}), 200
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:  
        return jsonify({"error": str(e)}), 500

@heidi_controller.route('/columns', methods=['GET']) 
def columns():
    datasetPath=request.args.get('datasetPath')
    print('Dataset path is ', datasetPath, 'in /columns api call')
    columns = getColumns(datasetPath)
    return jsonify({'columns': columns})

@heidi_controller.route('/image', methods=['POST'])
def heidi():
    # datasetPath=request.args.get('datasetPath')
    # #get list of dimensions from get request
    # orderingAlgorithm = request.args.get('orderingAlgorithm')
    # orderingDimensions = request.args.getlist('orderingDimensions')
    # selectedDimensions = request.args.getlist('selectedDimensions')
    
    data = request.get_json()
    datasetPath = data.get('datasetPath')
    orderingAlgorithm = data.get('orderingAlgorithm')
    orderingDimensions = data.get('orderingDimensions', [])  # This will be a list of strings
    selectedDimensions = data.get('selectedDimensions', [])  # This will also be a list of strings


    print('Dataset path is ', datasetPath, 'in /image api call', 'orderingAlgorithm is ', orderingAlgorithm, 'orderingDimensions is ', orderingDimensions, 'selectedDimensions is ', selectedDimensions)
    img, legend, sort_order, matrix_map = hd.getImage(datasetPath, selectedDimensions, orderingDimensions, orderingAlgorithm)
    
    # heidi_matrix = getHeidiMatrixForSubspaceList([selectedDimensions], datasetPath)
    
    # Convert the PIL image to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()
    matrix_map_serialized = {str(key): value.tolist() for key, value in matrix_map.items()}
    print(matrix_map_serialized.keys)
    response_data = {
        'status': 'success',
        'image': {
            'data': base64.b64encode(img_bytes).decode('utf-8'),
            'content_type': 'image/png'
        },
        'matrix_map': matrix_map_serialized,
        'sort_order': sort_order,
        'legend': legend.to_dict(orient="records")
    }
    return jsonify(response_data)

@heidi_controller.route('/consolidated-image', methods=['POST'])
def consolidated_heidi():
    data = request.get_json()
    datasetPath = data.get('datasetPath')
    orderingAlgorithm = data.get('orderingAlgorithm')
    selectedDimensions = data.get('selectedDimensions', [])  # This will also be a list of strings
    print('Dataset path is ', datasetPath, 'in /image api call', 'orderingAlgorithm is ', orderingAlgorithm, 'selectedDimensions is ', selectedDimensions)
    img, legend, sort_order, matrix_map = hd.getConsolidatedImage(datasetPath, selectedDimensions, orderingAlgorithm)
    
    # Convert the PIL image to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()
    
    response_data = {
        'status': 'success',
        'consolidated_image': {
            'data': base64.b64encode(img_bytes).decode('utf-8'),
            'content_type': 'image/png'
        },
        'sort_order': {},
        'legend': legend.to_dict(orient="records")
    }
    return jsonify(response_data)

@heidi_controller.route('/legend', methods=['GET'])
def getLegend():
    try:
        print('getLegend called')
        datasetPath = request.args.get('datasetPath')
        legend = hd.createLegend(datasetPath)
        # legend = legend.to_json(orient='records')
        return legend
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error in getting legend : ' + str(e)}), 500

@heidi_controller.route('/points', methods=['POST'])
def getPoints():
    try:
        print('getPoints called')
        data = request.get_json()
        datasetPath = data.get('datasetPath')
        orderingAlgorithm = data.get('orderingAlgorithm')
        orderingDimensions = data.get('orderingDimensions', [])  # This will be a list of strings
        selectedDimensions = data.get('selectedDimensions', [])  # This will also be a list of strings
        # matrix_map = data.get('matrix_map', {})
        rowPoint = data.get('rowPoint', '')
        colPoint = data.get('colPoint', '')
        print('Dataset path is ', datasetPath, 'in /image api call', 'orderingAlgorithm is ', orderingAlgorithm, 'orderingDimensions is ', orderingDimensions, 'selectedDimensions is ', selectedDimensions)
        
        img, legend, sort_order, matrix_map = hd.getImage(datasetPath, selectedDimensions, orderingDimensions, orderingAlgorithm)
        print('getting list of row and col points')
        points = hd.getPoints(datasetPath, matrix_map, rowPoint, colPoint)
        for subspace, df in points.items():
            df['rowPointValueSubspace'] = [ getPointValue(datasetPath, subspace, row_point) for row_point in df.loc[:,'row_point']]
            df['colPointValueSubspace'] = [ getPointValue(datasetPath, subspace, col_point) for col_point in df.loc[:,'col_point']]
            df['rowPointValue'] = [ getPointValue(datasetPath, None , row_point) for row_point in df.loc[:,'row_point']]
            df['colPointValue'] = [ getPointValue(datasetPath, None, col_point) for col_point in df.loc[:,'col_point']]
            
        #code to json serialize points dict
        points_serializable = {str(key): value.to_dict(orient='records') for key, value in points.items()}
        response_data = {
                        'status': 'success',
                        'points': points_serializable
                        }
        
        return response_data
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error in getting points : ' + str(e)}), 500
    

@heidi_controller.route('/subspace-comparison-matrix', methods=['GET'])
def getSubspaceOverlapMatrix():
    print('>>>> HeidiController : getSubspaceOverlapMatrix called.... ')
    data = request.args
    datasetPath = data.get('datasetPath')
    row_cluster = data.get('row_cluster')
    col_cluster = data.get('col_cluster')
    df = hd.getSubspaceOverlapMatrix(datasetPath, row_cluster, col_cluster)
    print(df.shape, df.columns)
    response_data = {
                    'status': 'success',
                    'data': df.to_dict(orient='records')
                    }
        
    return response_data
    
    
    
    
    