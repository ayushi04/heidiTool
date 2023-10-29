from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import config
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
login_manager = LoginManager()
login_manager.login_view = 'users.login'
app.config.from_object(config.DevelopmentConfig)

db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', user=current_user), 404

import models

with app.app_context():
    db.create_all()
    db.session.commit()
    print('created table!!')
        

    
    

        
    