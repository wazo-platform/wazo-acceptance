# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException

from xivo_lettuce.common import *
from xivo_lettuce.manager.group_manager import *
from xivo_lettuce.manager.context_manager import *


@step(u'Given there is no group with number "([^"]*)"')
def given_there_is_no_group_with_number(step, number):
    remove_group_with_number(number)


@step(u'Given there is no group with name "([^"]*)"')
def given_there_is_no_group_with_name(step, name):
    remove_group_with_name(name)


@step(u'When I create a group "([^"]*)" with number "([^"]*)"')
def when_i_create_group_with_number(step, group_name, group_number):
    check_context_number_in_interval('default', 'group', group_number)
    open_add_group_url()
    type_group_name(group_name)
    type_group_number(group_number)
    type_context('default')
    submit_form()


@step(u'When I create a group "([^"]*)"$')
def when_i_create_group(step, group_name):
    open_add_group_url()
    type_group_name(group_name)
    submit_form()


@step(u'When group "([^"]*)" is removed')
def when_group_is_removed(step, group_name):
    remove_group_with_name(group_name)


@step(u'Then group "([^"]*)" is displayed in the list')
def then_group_is_displayed_in_the_list(step, group_name):
    assert group_is_saved(group_name)


@step(u'Then group "([^"]*)" is not displayed in the list')
def then_group_is_not_displayed_in_the_list(step, group_name):
    assert not group_is_saved(group_name)
