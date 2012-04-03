# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException

from xivo_lettuce.common import *
from xivo_lettuce.common_steps import *


@step(u'Given there is no custom lines')
def given_there_is_no_custom_lines(step):
    remove_all_elements('line', 'Customized')


@step(u'Given there is a "([^"]*)" line$')
def given_there_is_a_sip_line(step, protocol):
    when_i_add_a_line(step,protocol.lower())
    when_i_set_the_context(step, 'default')
    world.id = world.browser.find_element_by_id('it-protocol-name').get_attribute('value')
    i_submit(step)


@step(u'When I add a "([^"]*)" line')
def when_i_add_a_line(step, protocol):
    open_url('line', 'add', {'proto': protocol.lower()})
    if protocol.lower() == 'sip':
        world.id = world.browser.find_element_by_id('it-protocol-name').get_attribute('value')


@step(u'When I set the context to "([^"]*)"')
def when_i_set_the_context(step, context):
    select_context = world.browser.find_element_by_xpath(
        '//select[@id="it-protocol-context"]//option[@value="%s"]' % context)
    select_context.click()


@step(u'When I set the interface to "([^"]*)"')
def when_i_set_the_interface(step, interface):
    input_interface = world.browser.find_element_by_id('it-protocol-interface')
    input_interface.send_keys(interface)


@step(u'When I remove this line')
def when_i_remove_this_line(step):
    remove_line(world.id)


@step(u'Then this line is displayed in the list')
def then_this_line_is_displayed_in_the_list(step):
    assert find_line(world.id) is not None


@step(u'Then this line is not displayed in the list')
def then_this_line_is_not_displayed_in_the_list(step):
    try:
        find_line(world.id)
    except NoSuchElementException:
        pass
    else:
        assert False
