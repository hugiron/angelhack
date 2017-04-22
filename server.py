from flask import Flask, session
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_debugtoolbar import DebugToolbarExtension
from datetime import timedelta

# Flask init
app = Flask(__name__)
app.config.from_pyfile('./config.py')

# Connection to database init
database = MongoEngine(app)
toolbar = DebugToolbarExtension(app)
app.session_interface = MongoEngineSessionInterface(database)
app.permanent_session_lifetime = timedelta(**app.config['SESSION_LIFETIME'])

# Start server
from route import *
if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])