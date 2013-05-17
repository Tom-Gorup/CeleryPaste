__author__ = 'pyt'

from CeleryPaste.core.models import Paste, paste_link
from CeleryPaste.core.settings import app
from flask.ext.couchdb import DateTimeField, CouchDBManager
import uuid

couch_manager = CouchDBManager()
# Doc
couch_manager.add_document(Paste)
couch_manager.add_viewdef(paste_link)

class DbCouch():
    PASTE_LINK_VIEW = '_design/paste/_view/link'
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = couch_manager.connect_db(app)
        return self._db

    def addPaste(self, _website, _link, _content):
        item_paste = Paste(
                website = _website,
                link = _link,
                content = _content
        )
        item_paste.id = uuid.uuid4().hex
        item_paste.store(db=self.db)
        return item_paste

    def returnAllLink(self):
        db_link = []
        result =  self.db.view(self.PASTE_LINK_VIEW)

        for _link_id in result:
            db_link.append(_link_id.key)
        return db_link
        #db_link = list()
        #for docId in self.db:
        #    db_link.append(self.db.get(docId)['link'])
        #return db_link

paste_database_couchdb = DbCouch()
