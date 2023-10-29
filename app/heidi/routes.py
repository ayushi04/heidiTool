from flask import Blueprint, jsonify, request, Response

from app.heidi.dataset.api import readDataset
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
    img = hd.getImage(datasetPath, selectedDimensions, orderingDimensions, orderingAlgorithm)
    
    # heidi_matrix = getHeidiMatrixForSubspaceList([selectedDimensions], datasetPath)
    
    # Convert the PIL image to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()
    
    response_data = {
        'status': 'success',
        'consolidated_image': {
            'data': base64.b64encode(img_bytes).decode('utf-8'),
            'content_type': 'image/png'
        }
    }

    
    return jsonify(response_data)

