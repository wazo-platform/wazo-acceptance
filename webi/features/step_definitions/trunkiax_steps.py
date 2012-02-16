# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

from xivo_lettuce.common import *
from xivo_lettuce.manager.trunkiax_manager import *


@step(u'Given there is no trunkiax "([^"]*)"')
def given_there_is_no_trunkiax(step, name):
    open_url('trunkiax', 'list')
    try:
        remove_line(name)
    except NoSuchElementException:
        pass


@step(u'When I create a trunkiax with name "([^"]*)"')
def when_i_create_a_trunkiax_with_name_and_trunk(step, name):
    open_url('trunkiax', 'add')
    input_name = world.browser.find_element_by_id('it-protocol-name', 'trunkiax form not loaded')
    input_name.send_keys(name)
    submit_form()


@step(u'Given there is a trunkiax "([^"]*)"')
def given_there_is_a_trunkiax(step, name):
    open_url('trunkiax', 'list')
    try:
        find_line(name)
    except NoSuchElementException:
        step.given(u'When I create an trunkiax with name "%s"' % (name))


@step(u'When I remove the trunkiax "([^"]*)"')
def when_i_remove_the_trunkiax(step, name):
    open_url('trunkiax', 'list')
    remove_line(name)
