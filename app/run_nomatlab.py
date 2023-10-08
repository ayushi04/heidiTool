# import sys
# sys.path.insert(0, '/Users/ayushigupta/Desktop/github/tq/TOOL')

#import matlab.engine
import os
from app import app
from app.config import DevelopmentConfig as config
from app.controllers import mod_controllers
from app.mod_dim.routes import heidi_controller

#eng = matlab.engine.start_matlab()
os.system('mkdir ' + config.STATIC_DIR)
os.system('mkdir ' + config.UPLOADS_DIR)
app.register_blueprint(mod_controllers)
app.register_blueprint(heidi_controller)

print('App ready to run')

app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
