import sys
sys.path.append("/Users/ayushigupta/Desktop/github/tq/TOOL")


#import matlab.engine 
import os
from app import app, db
from app.config import DevelopmentConfig as config
from app.controllers import mod_controllers
from app.heidi.routes import heidi_controller

#eng = matlab.engine.start_matlab()
os.system('mkdir ' + config.STATIC_DIR)
os.system('mkdir ' + config.UPLOADS_DIR)
os.system('mkdir ' + config.INTERMEDIATE_RESULT_DIR)
app.register_blueprint(mod_controllers)
app.register_blueprint(heidi_controller)

print('App ready to run')
app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

    
    
    