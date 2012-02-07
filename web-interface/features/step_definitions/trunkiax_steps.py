# -*- coding: utf-8 -*-

import time

from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException

from xivo_lettuce.common import *

trunkiax_URL = '/service/ipbx/index.php/trunk_management/iax/%s'

def _open_add_trunkiax_url():
    URL = trunkiax_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))


def _open_list_trunkiax_url():
    URL = trunkiax_URL % ('?act=list')
    world.browser.get('%s%s' % (world.url, URL))


@step(u'Given there is no trunkiax "([^"]*)"')
def given_there_is_no_trunkiax(step, name):
    _open_list_trunkiax_url()
    try:
        remove_line(name)
    except NoSuchElementException:
        pass


@step(u'When I create a trunkiax with name "([^"]*)"')
def when_i_create_a_trunkiax_with_name_and_trunk(step, name):
    _open_add_trunkiax_url()
    input_name = world.browser.find_element_by_id('it-protocol-name', 'trunkiax form not loaded')
    input_name.send_keys(name)
    submit_form()


@step(u'Then there is a trunkiax "([^"]*)"')
def then_there_is_a_trunkiax(step, name):
    _open_list_trunkiax_url()
    assert find_line(name) is not None


@step(u'Given there is a trunkiax "([^"]*)"')
def given_there_is_a_trunkiax(step, name):
    _open_list_trunkiax_url()
    try:
        find_line(name)
    except NoSuchElementException:
        step.given(u'When I create an trunkiax with name "%s"' % (name))


@step(u'When I remove the trunkiax "([^"]*)"')
def when_i_remove_the_trunkiax(step, name):
    _open_list_trunkiax_url()
    remove_line(name)


@step(u'Then there is no trunkiax "([^"]*)"')
def then_there_is_no_trunkiax(step, name):
    _open_list_trunkiax_url()
    try:
        find_line(name)
    except NoSuchElementException:
        pass
    else:
        assert False
