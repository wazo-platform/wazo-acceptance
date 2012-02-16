# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException

from xivo_lettuce.common import *
from xivo_lettuce.manager import line_manager as line_man


@step(u'When I create a "([^"]*)" line in context "([^"]*)"')
def when_i_create_a_line_in_context(step, protocol, context):
    open_url('line', 'add', {'proto': protocol.lower()})
    select_context = world.browser.find_element_by_xpath(
        '//select[@id="it-protocol-context"]//option[@value="%s"]' % context)
    select_context.click()
    # Get the id to reference the line
    world.id = world.browser.find_element_by_id('it-protocol-name').get_attribute('value')
    submit_form()


@step(u'When I remove this line')
def when_i_remove_this_line(step):
    remove_line(world.id)


@step(u'Given there is no SIP line "([^"]*)"')
def given_there_is_no_sip_line_1(step, line_number):
    line_man.delete_line_from_number(line_number)


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