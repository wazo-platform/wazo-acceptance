# -*- coding: utf-8 -*-

import time
import json
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException
from webservices.webservices import WebServicesFactory

QUEUE_URL = '/callcenter/index.php/settings/queues/%s'
WS = WebServicesFactory('callcenter/settings/queues')


def open_add_queue_form():
    URL = QUEUE_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))


def open_list_queue_url():
    URL = QUEUE_URL % '?act=list'
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('table-main-listing', 'Queue list not loaded')


def delete_queue_from_displayname(queue_displayname):
    for id in find_queue_id_from_displayname(queue_displayname):
        WS.delete(id)


def find_queue_id_from_displayname(queue_displayname):
    queue_list = WS.list()
    if queue_list:
        return [queueinfo['id'] for queueinfo in queue_list if
                queueinfo['displayname'] == queue_displayname]
    return []


def delete_queue_from_number(queue_number):
    for id in find_queue_id_from_number(queue_number):
        WS.delete(id)


def find_queue_id_from_number(queue_number):
    queue_list = WS.list()
    if queue_list:
        return [queueinfo['id'] for queueinfo in queue_list if
                queueinfo['number'] == queue_number]
    return []
