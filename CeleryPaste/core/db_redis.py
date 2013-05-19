__author__ = 'pyt'

from  CeleryPaste.core.settings import REDIS_DB, REDIS_PORT, REDIS_HOST
import redis
import base64

class DbRedis():
    _db = None

    def __init__(self):
        self.db_host = REDIS_HOST
        self.db_port = REDIS_PORT
        self.db_name = REDIS_DB

    @property
    def db(self):
        if self._db is None:
            self._db = redis.StrictRedis(host=self.db_host, port=self.db_port, db=self.db_name)
        return self._db

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

paste_database_redis = DbRedis()