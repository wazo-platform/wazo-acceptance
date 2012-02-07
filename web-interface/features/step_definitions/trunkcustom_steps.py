# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

from xivo_lettuce.common import *
from xivo_lettuce.ipbx_objects.user_manager import *

TRUNKCUSTOM_URL = '/service/ipbx/index.php/trunk_management/custom/%s'


def _open_add_trunkcustom_url():
    URL = TRUNKCUSTOM_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))


def _open_list_trunkcustom_url():
    URL = TRUNKCUSTOM_URL % ('?act=list')
    world.browser.get('%s%s' % (world.url, URL))


@step(u'Given there is a custom trunk "([^"]*)"')
def given_there_is_a_custom_trunk(step, name):
    _open_list_trunkcustom_url()
    try:
        find_line(name)
    except NoSuchElementException:
        _open_add_trunkcustom_url()
        input_name = world.browser.find_element_by_id('it-protocol-name', 'custom trunk form not loaded')
        input_name.send_keys(name)
        submit_form()


@step(u'Given there is no trunkcustom "([^"]*)"')
def given_there_is_no_trunkcustom(step, name):
    _open_list_trunkcustom_url()
    try:
        remove_line(name)
    except NoSuchElementException:
        pass


@step(u'When I create a trunkcustom with name "([^"]*)"')
def when_i_create_a_trunkcustom_with_name_and_trunk(step, name):
    _open_add_trunkcustom_url()
    input_name = world.browser.find_element_by_id('it-protocol-name', 'trunkcustom form not loaded')
    input_name.send_keys(name)
    input_interface = world.browser.find_element_by_id('it-protocol-interface', 'trunkcustom form not loaded')
    input_interface.send_keys('misdn//xivo')
    submit_form()


@step(u'Then there is a trunkcustom "([^"]*)"')
def then_there_is_a_trunkcustom(step, name):
    _open_list_trunkcustom_url()
    assert find_line(name) is not None


@step(u'Given there is a trunkcustom "([^"]*)"')
def given_there_is_a_trunkcustom(step, name):
    _open_list_trunkcustom_url()
    try:
        find_line(name)
    except NoSuchElementException:
        step.given(u'When I create an trunkcustom with name "%s"' % (name))


@step(u'When I remove the trunkcustom "([^"]*)"')
def when_i_remove_the_trunkcustom(step, name):
    _open_list_trunkcustom_url()
    remove_line(name)


@step(u'Then there is no trunkcustom "([^"]*)"')
def then_there_is_no_trunkcustom(step, name):
    _open_list_trunkcustom_url()
    try:
        find_line(name)
    except NoSuchElementException:
        pass
    else:
        assert False
