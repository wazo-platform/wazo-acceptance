# -*- coding: utf-8 -*-

from lettuce import step, world

from selenium.common.exceptions import NoSuchElementException
from xivo_lettuce.common import find_line, open_url, remove_line, submit_form


@step(u'Given there is a SIP trunk "([^"]*)"')
def given_there_is_a_sip_trunk(step, name):
    open_url('trunksip', 'list')
    try:
        find_line(name)
    except NoSuchElementException:
        open_url('trunksip', 'add')
        input_name = world.browser.find_element_by_id('it-protocol-name', 'SIP trunk form not loaded')
        input_name.send_keys(name)
        submit_form()


@step(u'Given there is no trunksip "([^"]*)"')
def given_there_is_no_trunksip(step, name):
    open_url('trunksip', 'list')
    try:
        remove_line(name)
    except NoSuchElementException:
        pass


@step(u'When I create a trunksip with name "([^"]*)"')
def when_i_create_a_trunksip_with_name_and_trunk(step, name):
    open_url('trunksip', 'add')
    input_name = world.browser.find_element_by_id('it-protocol-name', 'trunksip form not loaded')
    input_name.send_keys(name)
    submit_form()


@step(u'Given there is a trunksip "([^"]*)"')
def given_there_is_a_trunksip(step, name):
    open_url('trunksip', 'list')
    try:
        find_line(name)
    except NoSuchElementException:
        step.given(u'When I create an trunksip with name "%s"' % (name))


@step(u'When I remove the trunksip "([^"]*)"')
def when_i_remove_the_trunksip(step, name):
    open_url('trunksip', 'list')
    remove_line(name)
