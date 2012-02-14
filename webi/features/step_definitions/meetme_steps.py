# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException

from xivo_lettuce.common import *
from xivo_lettuce.manager.meetme_manager import *
from xivo_lettuce.manager.context_manager import *


@step(u'Then conference room "([^"]*)" is displayed in the list')
def then_conference_room_is_displayed_in_the_list(step, name):
    assert is_saved(name)


@step(u'Then conference room "([^"]*)" is not displayed in the list')
def then_conference_room_is_not_displayed_in_the_list(step, name):
    assert not is_saved(name)


@step(u'When I create a conference room with name "([^"]*)" with number "([^"]*)" with max participants "([^"]*)"')
def when_i_create_a_conference_room_with_name_number_max_participants(step, name, confno, maxusers):
    check_context_number_in_interval('default', 'meetme', confno)
    delete_all_meetme()
    open_add_form()
    type_name(name)
    type_context('default')
    type_confno(confno)
    type_maxusers(maxusers)
    submit_form()
