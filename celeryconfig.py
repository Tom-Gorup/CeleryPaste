__author__ = 'pyt'

import sys
import os
from datetime import timedelta

sys.path.insert(0, os.getcwd())


CELERY_SEND_EVENTS = True
CELERY_TASK_PUBLISH_RETRY = True
BROKER_HEARTBEAT = 30
BROKER_CONNECTION_RETRY = True
BROKER_CONNECTION_MAX_RETRIES = 100
BROKER_CONNECTION_TIMEOUT = 4
CELERY_CREATE_MISSING_QUEUES = True

BROKER_URL = "amqp://guest:@127.0.0.1//"
CELERY_IMPORTS = ("CeleryPaste.tasks.tasks", )
CELERY_RESULT_BACKEND = "amqp://guest:@127.0.0.1//"
CELERY_TIMEZONE = 'UTC'

CELERY_ROUTES = {
    'CeleryPaste.tasks.': {'queue': 'db'},
    'CeleryPaste.tasks.z': {'queue': 'garbber'},

}

CELERYBEAT_SCHEDULE = {
    'runs-every-3-minute': {
        'task': 'CeleryPaste.tasks..',
        'schedule': timedelta(minutes=2)
    },
}