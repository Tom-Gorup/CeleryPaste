__author__ = 'pyt'

from datetime import datetime
from couchdb.client import Document
from couchdb.mapping import TextField, DateTimeField

class Paste(Document):
    website = TextField()
    link = TextField()
    added = DateTimeField(default=datetime.now())
    content = TextField()