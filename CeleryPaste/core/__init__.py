__author__ = 'pyt'

import os

CeleryPaste_ROOT = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
COUCH_HOST = '127.0.0.1'
COUCH_PORT = 5984
COUCH_DB = 'pastes'
COUCH_USER = 'couchdb'
COUCH_PASS = ''
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = '0'