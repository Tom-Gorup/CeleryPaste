__author__ = 'pyt'

from CeleryPaste.tasks.grabers_tasks import (task_nopaste_grabber,
                                             task_pastebin_grabber,
                                             task_pastesite_grabber,
                                             task_pastie_grabber)
from CeleryPaste.tasks.download_tasks import task_download_pastes
from CeleryPaste.tasks.couchdb_tasks import task_prepare_redis
from CeleryPaste.tasks.redis_tasks import (task_add_downloaded_link_redis,
                                           task_check_link_redis,
                                           task_flushall_redis)
from threading import Event
from celery import group,chain
from time import sleep

class Scheduler():
    """Task scheduler."""
    def __init__(self):
        self._stopevent = Event()

    def run(self):
        self.init = task_flushall_redis.delay()
        sleep(1)
        if self.init.ready():
            self.redis = task_prepare_redis.delay()

        while not self._stopevent.isSet():
            if self.redis.ready():
                res_pastie = chain(task_pastie_grabber.s() |
                           task_check_link_redis.s() |
                           task_download_pastes.s() |
                           task_add_downloaded_link_redis.s()
                )
                res_nopaste = chain(task_nopaste_grabber.s() |
                                    task_check_link_redis.s() |
                                    task_download_pastes.s() |
                                    task_add_downloaded_link_redis.s()
                )
                res_pastebin = chain(task_pastebin_grabber.s() |
                                     task_check_link_redis.s() |
                                     task_download_pastes.s() |
                                     task_add_downloaded_link_redis.s()
                )
                # res_pastesite = chain(task_pastesite_grabber.s() |
                #                       task_check_link_redis.s() |
                #                       task_download_pastes.s() |
                #                       task_add_downloaded_link_redis.s()
                # )
                g_res = group(res_nopaste,
                              res_pastie,
                              res_pastebin,
                              # res_pastesite
                )
                g_res.apply_async()
                sleep(300)
            sleep(1)

    def stopped(self):
        return self._stopevent.isSet()

    def stop(self):
        self._stopevent.set()

    def end(self):
        task_flushall_redis.delay()


if __name__ == "__main__":
    schd = Scheduler()
    try:
        schd.run()
    except KeyboardInterrupt:
        print "KeyboardInterrupt send"
        schd.stop()
        sleep(5)
        print schd.stopped()
        schd.end()