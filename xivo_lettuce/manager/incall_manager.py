# -*- coding: utf-8 -*-

from lettuce import world
from selenium.webdriver.support.select import Select
from xivo_lettuce.common import remove_element_if_exist


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


def remove_incall_with_did_via_ws(incall_did):
    incalls = world.ws.incalls.search_by_number(incall_did)
    for incall in incalls:
        world.ws.incalls.delete(incall.id)
