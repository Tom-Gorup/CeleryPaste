__author__ = 'pyt'

# DB Couchdb
COUCHDB_SERVER="http://127.0.0.1:5984"
COUCHDB_DATABASE="paste"

# Redis
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = '0'

class AppSettings(object):
    config = {}
    def __init__(self):
        self.config['COUCHDB_SERVER'] = COUCHDB_SERVER
        self.config['COUCHDB_DATABASE'] = COUCHDB_DATABASE
        self.config['COUCHDB_USERNAME'] = ''
        self.config['COUCHDB_PASSWORD'] = ''

app = AppSettings()
