# -*- coding: utf-8 -*-

from lettuce.registry import world
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from xivo_lettuce.common import *

WS = get_webservices('incall')


def type_incall_did(incall_did):
    world.browser.find_element_by_id('it-incall-exten', 'Incall form not loaded')
    world.incall_did = incall_did
    input_did = world.browser.find_element_by_id('it-incall-exten')
    input_did.send_keys(incall_did)


def type_incall_context(incall_context):
    input_context = Select(world.browser.find_element_by_id('it-incall-context'))
    input_context.select_by_visible_text(incall_context)

def remove_incall_with_did(incall_did):
    remove_element_if_exist('incall', incall_did)
