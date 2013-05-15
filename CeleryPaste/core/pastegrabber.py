__author__ = 'pyt'

from lxml.etree import HTMLParser, parse
import requests
from random import choice
from celery.app.log import get_logger
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

logger = get_logger(__name__)
DEBUG = True

USER_AGENTS = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
]

class PasteGraber(object):
    def __init__(self, grabber_name, paste_url, query_url, links_xpath, links_post_process=None):
        self.grabber_name = grabber_name
        self.paste_url = paste_url
        self.query_url = query_url
        self.links_xpath = links_xpath
        self.links_post_process = links_post_process

    def run(self):
            list_turples = list()
            try:
                if self.checkConnection():
                    data = requests.get(self.paste_url)
                    parser = HTMLParser(encoding='utf8')
                    tree = parse(StringIO(data.content), parser)
                    root = tree.getroot()
                    links = root.xpath(self.links_xpath)
                    if self.links_post_process is not None:
                        links = map(self.links_post_process, links)
                    for l in links:
                        que_url = self.query_url % l
                        worker_turple = (self.grabber_name, que_url)
                        list_turples.append(worker_turple)
                else:
                    return None

            except Exception, e:
                msg = "%s: Exception running scraper [%s]" % (
                    self.grabber_name, str(e)
                    )
                logger.error(msg)
                return None

            if DEBUG:
                logger.debug("%s: list turples: %s " % (self.grabber_name, list_turples))

            return list_turples

    def headers(self):
        headers = {'User-Agent': choice(USER_AGENTS)}
        return headers

    def checkConnection(self):
        try:
            response = requests.get(self.paste_url, headers=self.headers())
            if response.status_code is 200:
                return True
            else:
                return False
        except Exception:
            logger.warn('No connection')
            return False

