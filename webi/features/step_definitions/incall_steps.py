# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException

from xivo_lettuce.common import *
from xivo_lettuce.manager.context_manager import *
from xivo_lettuce.manager.incall_manager import *


@step(u'Given there is no incall with DID "([^"]*)"')
def given_there_is_no_incall_with_did(step, did):
    remove_incall_with_did(did)


@step(u'When I create an incall with DID "([^"]*)"')
def when_i_create_incall_with_did(step, incall_did):
    check_context_number_in_interval('from-extern', 'incall', incall_did)
    open_add_incall_url()
    type_incall_did(incall_did)
    submit_form()


@step(u'When incall "([^"]*)" is removed')
def when_incall_is_removed(step, incall_did):
    remove_incall_with_did(incall_did)


@step(u'Then incall "([^"]*)" is displayed in the list')
def then_incall_is_displayed_in_the_list(step, incall_did):
    assert incall_is_saved(incall_did)


@step(u'Then incall "([^"]*)" is not displayed in the list')
def then_incall_is_not_displayed_in_the_list(step, incall_did):
    assert not incall_is_saved(incall_did)
