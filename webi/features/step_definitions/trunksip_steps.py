# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

from xivo_lettuce.common import *
from xivo_lettuce.manager.user_manager import *
from xivo_lettuce.manager.trunksip_manager import *


@step(u'Given there is no SIP trunk')
def given_there_is_no_sip_trunk(step):
    delete_all_trunksip()


@step(u'Given there is a SIP trunk "([^"]*)"')
def given_there_is_a_sip_trunk(step, name):
    open_list_trunksip_url()
    try:
        find_line(name)
    except NoSuchElementException:
        open_add_trunksip_url()
        input_name = world.browser.find_element_by_id('it-protocol-name', 'SIP trunk form not loaded')
        input_name.send_keys(name)
        submit_form()


@step(u'Given there is no trunksip "([^"]*)"')
def given_there_is_no_trunksip(step, name):
    open_list_trunksip_url()
    try:
        remove_line(name)
    except NoSuchElementException:
        pass


@step(u'When I create a trunksip with name "([^"]*)"')
def when_i_create_a_trunksip_with_name_and_trunk(step, name):
    open_add_trunksip_url()
    input_name = world.browser.find_element_by_id('it-protocol-name', 'trunksip form not loaded')
    input_name.send_keys(name)
    submit_form()


@step(u'Then there is a trunksip "([^"]*)"')
def then_there_is_a_trunksip(step, name):
    open_list_trunksip_url()
    assert find_line(name) is not None


@step(u'Given there is a trunksip "([^"]*)"')
def given_there_is_a_trunksip(step, name):
    open_list_trunksip_url()
    try:
        find_line(name)
    except NoSuchElementException:
        step.given(u'When I create an trunksip with name "%s"' % (name))


@step(u'When I remove the trunksip "([^"]*)"')
def when_i_remove_the_trunksip(step, name):
    open_list_trunksip_url()
    remove_line(name)


@step(u'Then there is no trunksip "([^"]*)"')
def then_there_is_no_trunksip(step, name):
    open_list_trunksip_url()
    try:
        find_line(name)
    except NoSuchElementException:
        pass
    else:
        assert False
