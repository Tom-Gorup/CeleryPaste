CeleryPaste v0.3
================

PasteGraber with celery to download Paste on differents website (e.g: pastebin.com, nopaste.org).

How to install
--------------

On ubuntu 13.04 :

    $ sudo apt-get install python-dev python-pip python-lxml couchdb redis-server git rabbitmq-server

    $ pip install requests celery simplejson flask couchdb redis

For starting the worker :

    # pyt at DELL-P1128 in /opt/test/CeleryPaste on git:master o [23:19:29]
    $ ll
    total 40
    -rw-rw-r-- 1 pyt pyt  1147 mai   18 18:42 celeryconfig.py
    drwxrwxr-x 6 pyt pyt  4096 mai   19 23:19 CeleryPaste
    -rw-rw-r-- 1 pyt pyt  2848 mai   19 13:23 celery_scraper.py
    -rw-rw-r-- 1 pyt pyt   359 mai   18 18:09 README.md
    drwxrwxr-x 4 pyt pyt  4096 mai   18 18:09 script

    $ celery worker -E --config=celeryconfig  --loglevel=DEBUG --concurrency=4

And finally launch the tasks:

    $ python celery_scraper.py

dev ongoing !
-------------

