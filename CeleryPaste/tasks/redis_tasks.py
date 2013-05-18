__author__ = 'pyt'

from CeleryPaste.core.db_redis import paste_database_redis
from CeleryPaste.celeryctl import celery

@celery.task
def task_check_link_redis(infos_turples):
    return paste_database_redis.checkListLink(infos_turples)

@celery.task
def task_flushall_redis():
    return paste_database_redis.flushallRedis()

@celery.task
def task_add_downloaded_link_redis(info_turples):
    listtopass = list()
    for li in info_turples:
        link, boolli = li
        if boolli:
            listtopass.append(link)
    paste_database_redis.chargeLinkInRedis(listtopass)
