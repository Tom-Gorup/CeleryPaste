__author__ = 'pyt'

from CeleryPaste.core.db_couch import paste_database_couchdb
from CeleryPaste.core.db_redis import paste_database_redis
from CeleryPaste.celeryctl import celery


@celery.task
def task_prepare_redis():
    link = paste_database_couchdb.returnAllLink()
    paste_database_redis.chargeLinkInRedis(link)

