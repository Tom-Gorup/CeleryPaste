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
        '//div[@class="grid_3 info"][position() = 1]/a/@href',
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
        '//table[@class="maintable"]//td[position() = 1]//a/@href',
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