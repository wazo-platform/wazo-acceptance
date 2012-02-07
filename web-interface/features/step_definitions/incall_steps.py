# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException

from xivo_lettuce.common import *

INCALL_URL = '/service/ipbx/index.php/call_management/incall/%s'


def _open_add_incall_url():
    URL = INCALL_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('it-incall-exten', 'Incall form not loaded')


def _open_list_incall_url():
    URL = INCALL_URL % ('?act=list')
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('table-main-listing', 'Incall list not loaded')


def _type_incall_did(incall_did):
    world.browser.find_element_by_id('it-incall-exten', 'Incall form not loaded')
    world.incall_did = incall_did
    input_did = world.browser.find_element_by_id('it-incall-exten')
    input_did.send_keys(incall_did)


def _remove_incall_with_did(incall_did):
    _open_list_incall_url()
    try:
        remove_line(incall_did)
    except NoSuchElementException:
        pass


def _incall_is_saved(incall_did):
    _open_list_incall_url()
    try:
        incall = find_line(incall_did)
        return incall is not None
    except NoSuchElementException:
        return False


@step(u'Given there is no incall with DID "([^"]*)"')
def given_there_is_no_incall_with_did(step, did):
    _remove_incall_with_did(did)


@step(u'When I create an incall with DID "([^"]*)"')
def when_i_create_incall_with_did(step, incall_did):
    import context_steps as ctx
    ctx.when_i_edit_a_context(step, 'from-extern')
    ctx.when_i_edit_incall_ranges(step)
    ctx.when_i_add_incall_interval(step, 6000, 7000, '4')
    _open_add_incall_url()
    _type_incall_did(incall_did)
    submit_form()


@step(u'When incall "([^"]*)" is removed')
def when_incall_is_removed(step, incall_did):
    _remove_incall_with_did(incall_did)


@step(u'Then incall "([^"]*)" is displayed in the list')
def then_incall_is_displayed_in_the_list(step, incall_did):
    assert _incall_is_saved(incall_did)


@step(u'Then incall "([^"]*)" is not displayed in the list')
def then_incall_is_not_displayed_in_the_list(step, incall_did):
    assert not _incall_is_saved(incall_did)
