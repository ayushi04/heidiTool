from flask import request, render_template, Blueprint, json, redirect, url_for, flash
from app import db, login_manager
from app.heidi.dataset.api import readDataset
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.utils import secure_filename
import random
import os
import pandas as pd
from config import DevelopmentConfig as config
from mod_datacleaning import data_cleaning
import app.heidi.api as hd
import app.heidi.database.api as heidi_db
from flask import jsonify
import linecache
import sys

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    return ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

mod_controllers = Blueprint('controllers', __name__)

#To create new user (name, phone number, password) and save it in database
@mod_controllers.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            user = User(request.form['name'], request.form['phone'], generate_password_hash(
                request.form['password'], method='sha256'), request.form['email'])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('controllers.login'))
        except Exception as e:
            print(e)
            flash('Wrong inputs, please check your input and try again.')
            return render_template('register.html', user=current_user)
    else:
        return render_template('register.html', user=current_user)


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None


@mod_controllers.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        if not current_user.is_anonymous:
            return render_template('index.html', user=current_user)
        return render_template('login.html', user=current_user)
    else:
        user = User.query.filter(User.email == request.form['email']).first()
        if user:
            if check_password_hash(user.password, request.form['password']):
                login_user(user)
                return render_template('index.html', user=current_user)
            else:
                flash('Wrong password.')
                return render_template('login.html', user=current_user)
        else:
            flash('Username doesn\'t exist.')
            return render_template('login.html', user=current_user)


@mod_controllers.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('controllers.index'))


@mod_controllers.route('/', methods=['GET'])
def index():
    return render_template('index.html', user=current_user)


@mod_controllers.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files.get('file')
        if not file or file.filename == '':
            raise ValueError('No file uploaded!!')

        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        if file_extension not in {'csv', 'tsv', 'json'}:
            raise ValueError('Invalid file input! Please check the input file type')

        os.makedirs(config.UPLOADS_DIR, exist_ok=True)
        file_uploads_path = os.path.join(config.UPLOADS_DIR, filename)
        file.save(file_uploads_path)

        fix_method = request.form.get('fix', '')
        dirty_file = _load_uploaded_dataframe(file_uploads_path, file_extension)

        if file_extension == 'csv':
            id_check = data_cleaning.id_classLabel_check(dirty_file)
            if id_check is not True:
                raise ValueError(id_check)

        cleaned_file = _clean_uploaded_dataframe(dirty_file, fix_method)
        _persist_cleaned_dataframe(cleaned_file, file_uploads_path, file_extension)

        download_path = 'static/uploads/' + filename
        
        robj = readDataset(download_path)
        heidi_db.saveDatasetToDB(download_path)
        hd.createAndSaveMatrixToDB(download_path, 5)
        response_data = {
            'status': 'success',
            'datasetPath': download_path,
            'url': '/columns',  # This should be the URL for the columns display page
            
        }
        return jsonify(response_data)
    
        # return render_template('success.html', download_path=download_path, user=current_user)
        # return render_template('first.html',title='visual tool',datasetPath=download_path, user=current_user)
    except Exception as e:
        print(e)
        error_message = PrintException()
        flash(error_message)
        return render_template('index.html', user=current_user)


def _load_uploaded_dataframe(file_path, extension):
    if extension == 'csv':
        return pd.read_csv(file_path, sep=',')
    if extension == 'tsv':
        return pd.read_csv(file_path, sep='\t')
    if extension == 'json':
        return pd.read_json(file_path)
    raise ValueError('Unsupported file extension')


def _clean_uploaded_dataframe(dataframe, fix_method):
    """
    Applies the cleaning pipeline to the uploaded dataset.
    """
    missing_val_fixed_file = data_cleaning.fix_missing(dataframe, fix_method)
    return data_cleaning.clean(missing_val_fixed_file)


def _persist_cleaned_dataframe(dataframe, destination_path, extension):
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    if extension == 'json':
        dataframe.to_json(destination_path)
    else:
        dataframe.to_csv(destination_path, sep=',', index=False)

@mod_controllers.route('/contact', methods=['GET'])
def contact():
    print(current_user.name)
    return render_template('contact.html', user=current_user)


@login_required
@mod_controllers.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'GET':
        colors = ['primary', 'success', 'info', 'warning', 'danger']
        return render_template('account.html', user=current_user, color=random.choice(colors))
    else:
        try:
            if check_password_hash(current_user.password, request.form['oldpassword']):
                current_user.password = generate_password_hash(
                    request.form['newpassword'], method='sha256')
                db.session.commit()
                return redirect(url_for('controllers.index'))
            else:
                flash('Enter current password correctly and try again.')
                return redirect(url_for('controllers.account'))
        except:
            flash('Some error occurred, please try again later.')
            return redirect(url_for('controllers.account'))
