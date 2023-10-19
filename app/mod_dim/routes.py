from flask import Blueprint, jsonify, request

from app.heidi.upload import readDataset
from app.mod_dim.helper.readDataset import ReadDatasetCls
from app.heidi.upload import saveMatrixToDB
import app.heidi.database as database
from app.heidi.fetch import *


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
        robj=ReadDatasetCls()
        robj.readDataset(datasetPath)
        database.save_dataset_to_db(robj)
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
    # robj=ReadDatasetCls()
    # robj.readDataset(datasetPath)
    # columns = robj.getColumNames()
    columns = getColumns(datasetPath)
    return jsonify({'columns': columns})

@heidi_controller.route('/image', methods=['GET'])
def heidi():
    datasetPath=request.args.get('datasetPath')
    #get list of dimensions from get request
    orderingAlgorithm = request.args.getlist('orderingAlgorithm')
    orderingDimensions = request.args.getlist('orderingDimensions')
    selectedDimensions = request.args.getlist('selectedDimensions')
    print('Dataset path is ', datasetPath, 'in /image api call', 'orderingAlgorithm is ', orderingAlgorithm, 'orderingDimensions is ', orderingDimensions, 'selectedDimensions is ', selectedDimensions)
    robj = ReadDatasetCls()
    robj.readDataset(datasetPath)
    print('dataset read successfully')
    heidi_matrix = getHeidiMatrixForListofSubsetofDimensions([selectedDimensions], robj)
    print(heidi_matrix)
    return jsonify({'heidi_matrix': heidi_matrix.tolist()})

