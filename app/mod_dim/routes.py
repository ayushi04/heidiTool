from flask import Blueprint, jsonify, request

from app.mod_dim.createHeidi import readDataset
from app.mod_dim.helper.readDataset import ReadDatasetCls
from app.mod_dim.createHeidi import saveMatrixToDB
import app.mod_dim.fetch as fetch

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
        fetch.save_dataset_to_db(robj)
        data = saveMatrixToDB(robj)
        return jsonify({"data": data.to_dict(orient="records")}), 200
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:  
        return jsonify({"error": str(e)}), 500

