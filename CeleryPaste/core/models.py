__author__ = 'pyt'

from CeleryPaste.ext.flaskcouchdb.couchdb import Document, TextField, DateTimeField, ViewDefinition
from datetime import datetime

class Paste(Document):
    website = TextField()
    link = TextField()
    added = DateTimeField(default=datetime.utcnow)
    content = TextField()

paste_link = ViewDefinition('paste', 'link', '''\
    function(doc) {
        if((doc.link != null) && (doc.content != null))
            emit(doc.link, doc._id);
    }'''
)