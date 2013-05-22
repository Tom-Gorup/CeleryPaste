__author__ = 'pyt'

from CeleryPaste.core.pastegrabber import PasteGraber
from CeleryPaste.celeryctl import celery

@celery.task
def task_pastie_grabber():
        pastie_grabber = PasteGraber(
            "pastie.org","http://pastie.org/pastes",
            'http://pastie.org/pastes/%s/text',
            '//div[@id="content"]//p[@class="link"]/a/@href',
            links_post_process=lambda i: i.split('/')[-1]
        )
        run = pastie_grabber.run()
        if run is None:
            raise task_pastie_grabber.retry(countdown=60)
        return run


@celery.task
def task_nopaste_grabber():
    nopaste_grabber = PasteGraber(
        'nopaste.me', 'http://nopaste.me/recent',
        "http://nopaste.me/raw/%s",
        '//div[@class="grid_12 entry"]/div[@class="grid_3 info"][position() = 1]/a/@href',
        links_post_process=lambda i: i.split('/')[-1]
    )
    run = nopaste_grabber.run()
    if run is None:
        raise task_nopaste_grabber.retry(countdown=60)
    return run

@celery.task
def task_pastebin_grabber():
    pastebin_grabber = PasteGraber(
        'pastebin.com','http://pastebin.com/archive',
        'http://pastebin.com/raw.php?i=%s',
        '//table[@class="maintable"]//tr/td[position() = 1]//a/@href',
        links_post_process=lambda i: i[1:]
    )
    run = pastebin_grabber.run()
    if run is None:
        raise task_pastebin_grabber.retry(countdown=60)
    return run

@celery.task
def task_pastesite_grabber():
    pastesite_grabber = PasteGraber(
        'pastesite.com','http://pastesite.com/recent',
        "http://pastesite.com/plain/%s",
        '//div[@id="full-width"]/h3/a/@href'
    )
    run = pastesite_grabber.run()
    if run is None:
        raise task_pastesite_grabber.retry(countdown=60)
    return run

@celery.task
def task_pastebinca_grabber():
    pastebinca_grabber = PasteGraber(
           "pastebin.ca","http://pastebin.ca",
           'http://pastebin.ca/raw/%s',
           '//div[@id="idmenurecent-collapse"]//a/@href',
            links_post_process=lambda i: i.split('/')[-1]
    )
    run = pastebinca_grabber.run()
    if run is None:
        raise task_pastebinca_grabber.retry(countdown=60)
    return run

@celery.task
def task_pastefrubar_net_grabber():
    pastef_rubar_net_grabber = PasteGraber(
           "paste.frubar.net","http://paste.frubar.net/",
            'http://paste.frubar.net/download/%s',
           '//div[@id="menu"]/ul[1]/li/a/@href',
            links_post_process=lambda i: i.split('/')[-1]
    )
    run = pastef_rubar_net_grabber.run()
    if run is None:
        raise task_pastefrubar_net_grabber.retry(countdown=60)
    return run


@celery.task
def task_paste_is_grabber():
    paste_is_grabber = PasteGraber(
           "paste.is","http://paste.is/all/",
            'http://paste.is/%s/raw/',
           '//div[@class="visible"]//a/@href',
            links_post_process=lambda i: i.split('/')[1]
    )
    run = paste_is_grabber.run()
    if run is None:
        raise task_paste_is_grabber.retry(countdown=60)
    return run

@celery.task
def task_paste_ie_grabber():
    paste_ie_grabber = PasteGraber(
           "paste.ie","http://paste.ie/lists",
            'http://paste.ie/view/raw/%s',
           '//table[@class="recent"]//a/@href',
            links_post_process=lambda i: i.split('/')[-1]
    )
    run = paste_ie_grabber.run()
    if run is None:
        raise task_paste_ie_grabber.retry(countdown=60)
    return run

