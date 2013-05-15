__author__ = 'pyt'

from CeleryPaste.core import COUCH_DB,COUCH_PASS,COUCH_USER,COUCH_HOST,COUCH_PORT,REDIS_DB,REDIS_PORT,REDIS_HOST
import couchdb
import redis
import base64

class DbCouch():
    def __init__(self):
        self.db_host = COUCH_HOST
        self.db_port = COUCH_PORT
        self.db_name = COUCH_DB
        self.db = None
        self.initDb()

    def initDb(self):
        self.server = couchdb.Server(url='http://%s:%s' % (self.db_host, self.db_port))
        self.server.resource.credentials = (COUCH_USER, COUCH_PASS)
        try:
            self.db = self.server[str(self.db_name)]
        except:
            self.db  = self.server.create(str(self.db_name))

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
        db_link = list()
        for docId in self.db:
            db_link.append(self.db.get(docId)['link'])
        return db_link

class DbRedis():
    def __init__(self):
        self.db_host = REDIS_HOST
        self.db_port = REDIS_PORT
        self.db_name = REDIS_DB
        self.db = None
        self.initDb()

    def initDb(self):
        self.db = redis.StrictRedis(host=self.db_host, port=self.db_port, db=self.db_name)

    def chargeLinkInRedis(self, db_link):
        for li in db_link:
            encodeLink = base64.b64encode(li)
            self.db.set(encodeLink, 'True')

    def presentLink(self, link):
        return self.db.exists(base64.b64encode(link))

    def checkListLink(self, list_paste):
        returnList = list()
        for paste in list_paste:
            web, link = paste
            if not self.presentLink(link):
                returnList.append(paste)
        return returnList

    def flushallRedis(self):
        return self.db.flushall()


