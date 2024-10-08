from flask import request, render_template, Blueprint, json, redirect, url_for, flash
from app import db, login_manager
from heidi.database.fetch import *
from app.heidi.dataset.api import readDataset
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user
import random
#import matlab.engine
from flask import jsonify
import os
import pandas as pd
import app.config as config
import time
import matplotlib.pyplot as plt

mod_heidicontrollers = Blueprint('heidicontrollers', __name__, url_prefix='/heidi')

# @mod_heidicontrollers.route('/heidi')
# def heidi():
#     datasetPath=request.args.get('datasetPath')
#     #get list of dimensions from get request
#     dimensions = request.args.getlist('dimensions')
#     orderDimensions = request.args.getlist('orderDimensions')
    
#     datasetObj = readDataset(datasetPath)
#     heidi_matrix = getHeidiMatrixForListofSubsetofDimensions(dimensions, datasetObj)
    
#     return jsonify({'heidi_matrix': heidi_matrix.tolist()})
    
#     # return render_template('dimension.html',title='dimension Visualization',datasetPath=datasetPath,user=current_user)


