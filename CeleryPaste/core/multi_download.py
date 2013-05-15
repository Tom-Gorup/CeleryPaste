__author__ = 'pyt'

from CeleryPaste.core.models import Paste
from CeleryPaste.core.database import DbCouch
from Queue import Queue
from threading import Thread
from random import choice
import requests
import logging

requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)

USER_AGENTS = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
]

class FileDownloader(Thread):
    """Threaded file downloader."""

    def __init__(self, infos_tuple):
        # infos_tuple is a 2-tuples tuple containing name, the file url
        self.website, self.url = infos_tuple
        self.initdb = DbCouch()
        self.db = self.initdb.db
        self.result = None
        self.response = None
        super(FileDownloader, self).__init__()

    def run(self):
        try:
        #if not self.checkExistingLink():
            # download
            self.response = requests.get(self.url, headers=self.headers(),)
            # DB
            paste = Paste()
            paste['website'] = unicode(self.website)
            paste['link'] = unicode(self.url)
            paste['content'] = unicode(self.response.text)
            #paste['added'] = datetime.now()
            self.db.save(paste)
        #else:
            #self.result = (self.url, 'Already')
            #return

        except Exception as err:
            print err.args
            self.result = (self.url, False)
            return

        self.result = (self.url, True)

    def headers(self):
        headers = {'User-Agent': choice(USER_AGENTS)}
        return headers


class MultiFileDownloader(object):
    """Downloads multiple files in multiple parallels threads."""
    def __init__(self, infos_tuples):
        self.infos_tuples = infos_tuples
        self.results = []
        self.queue = Queue(4)

    def start(self):
        def producer():
            """Feed the queue with FileDownloader instances."""
            for infos_tuple in self.infos_tuples:
                thread = FileDownloader(infos_tuple)
                thread.start()
                self.queue.put(thread)
        def consumer():
            """Gather results from FileDownloader instances in the queue."""
            while len(self.results) < len(self.infos_tuples):
                thread = self.queue.get()
                thread.join()
                self.results.append(thread.result)
        self._tprod = Thread(target=producer)
        self._tcons = Thread(target=consumer)
        self._tprod.start()
        self._tcons.start()

    def join(self):
        self._tprod.join()
        self._tcons.join()



