__author__ = 'pyt'

from CeleryPaste.core.models import Paste, paste_link
from CeleryPaste.core.settings import app
from flask.ext.couchdb import CouchDBManager
import uuid

class DbCouch():
    PASTE_LINK_VIEW = '_design/paste/_view/link'
    _db = None

    def __init__(self):
        self.couch_manager = CouchDBManager()
        self.couch_manager.add_document(Paste)
        self.couch_manager.add_viewdef(paste_link)

    @property
    def db(self):
        if self._db is None:
            self._db = self.couch_manager.connect_db(app)
        return self._db

    def addPaste(self, _website, _link, _content):
        item_paste = Paste(
            website=_website,
            link=_link,
            content=_content
        )
        item_paste.id = uuid.uuid4().hex
        item_paste.store(db=self.db)
        return item_paste

    def returnAllLink(self):
        db_link = []
        result = self.db.view(self.PASTE_LINK_VIEW)

        for _link_id in result:
            db_link.append(_link_id.key)
        return db_link

paste_database_couchdb = DbCouch()
