# -*- coding: utf-8 -*-

from lettuce import world
from selenium.webdriver.support.select import Select
from xivo_lettuce import common


def type_incall_did(incall_did):
    world.browser.find_element_by_id('it-incall-exten', 'Incall form not loaded')
    world.incall_did = incall_did
    input_did = world.browser.find_element_by_id('it-incall-exten')
    input_did.send_keys(incall_did)


def type_incall_context(incall_context):
    input_context = Select(world.browser.find_element_by_id('it-incall-context'))
    input_context.select_by_visible_text(incall_context)


def type_incall_queue(queue_name):
    type_select = Select(world.browser.find_element_by_id('it-dialaction-answer-actiontype'))
    type_select.select_by_visible_text("Queue")
    destination_select = Select(world.browser.find_element_by_id('it-dialaction-answer-queue-actionarg1'))
    for option in destination_select.options:
        if queue_name in option.text:
            destination_select.select_by_visible_text(option.text)


def type_incall_caller_id(caller_id):
    mode_select = Select(world.browser.find_element_by_id('it-callerid-mode'))
    mode_select.select_by_visible_text('Overwrite')
    caller_id_field = world.browser.find_element_by_id('it-callerid-callerdisplay')
    caller_id_field.send_keys(caller_id)


def remove_incall_with_did(incall_did):
    common.remove_element_if_exist('incall', incall_did)
