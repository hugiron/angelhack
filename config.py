HOST = '0.0.0.0'
PORT = 8081

DEBUG = True
SECRET_KEY = 'Tkrkje(0p{C"uR+i.4sVY,uS>K.5d/8g'
SESSION_LIFETIME = dict(days=365)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'vk4me'
MONGODB_USERNAME = 'spylogger'
MONGODB_PASSWORD = 'Re85wwBA5C6JSzp4'

DEBUG_TB_PANELS = [
    'flask_mongoengine.panels.MongoDebugPanel'
]
DEBUG_TB_INTERCEPT_REDIRECTS = False
