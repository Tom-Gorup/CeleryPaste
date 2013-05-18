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

BROKER_URL = "librabbitmq://guest:@127.0.0.1//"
CELERY_IMPORTS = ("CeleryPaste.tasks.couchdb_tasks",
                  "CeleryPaste.tasks.download_tasks",
                  "CeleryPaste.tasks.grabers_tasks",
                  "CeleryPaste.tasks.redis_tasks"
)

CELERY_RESULT_BACKEND = "librabbitmq://guest:@127.0.0.1//"
CELERY_TIMEZONE = 'UTC'

CELERY_ROUTES = {
    'CeleryPaste.tasks.couchdb_tasks': {'queue': 'db'},
    'CeleryPaste.tasks.download_tasks': {'queue': 'download'},
    'CeleryPaste.tasks.grabers_tasks': {'queue': 'grabers'},
    'CeleryPaste.tasks.redis_tasks': {'queue': 'db'},
}

CELERY_CREATE_MISSING_QUEUES = True

CELERYBEAT_SCHEDULE = {
    'runs-every-6-minute': {
        'task': 'celerybeat.Scraper.run',
        'schedule': timedelta(minutes=6)
    },
}