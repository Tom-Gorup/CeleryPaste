__author__ = 'pyt'

from CeleryPaste.core.multi_download import MultiFileDownloader
from CeleryPaste.celeryctl import celery

@celery.task
def task_download_pastes(info_turples):
    mfd = MultiFileDownloader(info_turples)
    mfd.start()
    mfd.join()
    return mfd.results