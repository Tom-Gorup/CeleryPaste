__author__ = 'pyt'

from CeleryPaste.core.models import Paste, paste_link
from CeleryPaste.core.settings import app
from flask.ext.couchdb import DateTimeField, CouchDBManager


couch_manager = CouchDBManager()
# Doc
couch_manager.add_document(Paste)
couch_manager.add_viewdef(paste_link)

class DbCouch():
    PASTE_LINK = '_design/paste/_view/link'
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = couch_manager.connect_db(app)
        return self._db

    def checkExistingLink(self, list_paste):
        db_link = list()
        for docId in self.db:
            db_link.append(self.db.get(docId)['link'])

        returnList = list()
        for paste in list_paste:
            web, link = paste
            boolInPlace = unicode(link) in db_link
            if not boolInPlace:
                returnList.append(paste)

        return returnList

    def returnAllLink(self):
        
        #db_link = list()
        #for docId in self.db:
        #    db_link.append(self.db.get(docId)['link'])
        #return db_link


paste_database = DbCouch()
