# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException

from common.common import submit_form


MM_URL = '/service/ipbx/index.php/pbx_settings/meetme/%s'

def _open_add_form():
    URL = MM_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))
    world.wait_for_id('it-meetmefeatures-name', 'Meetme add form not loaded')


def _open_edit_form(id):
    URL = MM_URL % '?act=edit&id=%d'
    world.browser.get('%s%s' % (world.url, URL % id))
    world.wait_for_id('it-meetmefeatures-name', 'Meetme edit form not loaded')


def _open_list_url():
    URL = MM_URL % '?act=list'
    world.browser.get('%s%s' % (world.url, URL))
    world.wait_for_id('table-main-listing', 'Meetme list not loaded')


def _type_name(name):
    world.wait_for_id('it-meetmefeatures-name', 'Meetme form not loaded')
    input_name = world.browser.find_element_by_id('it-meetmefeatures-name')
    input_name.clear()
    input_name.send_keys(name)


def _type_confno(confno):
    world.wait_for_id('it-meetmefeatures-confno', 'Meetme form not loaded')
    input_confno = world.browser.find_element_by_id('it-meetmefeatures-confno')
    input_confno.clear()
    input_confno.send_keys(confno)


def _type_context(context):
    world.wait_for_id('it-meetmefeatures-context', 'Meetme form not loaded')
    language_option = world.browser.find_element_by_xpath('//select[@id="it-meetmefeatures-context"]//option[@value="%s"]' % context)
    language_option.click()


def _type_maxusers(maxusers):
    world.wait_for_id('it-meetmefeatures-maxusers', 'Meetme form not loaded')
    input_maxusers = world.browser.find_element_by_id('it-meetmefeatures-maxusers')
    input_maxusers.clear()
    input_maxusers.send_keys(maxusers)

def _delete_all_meetme():
    from webservices.meetme import WsMeetme
    wsm = WsMeetme()
    wsm.clear()

def _is_saved(name):
    _open_list_url()
    try:
        meetme = world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s')]" % (name))
        return meetme is not None
    except NoSuchElementException:
        return False


@step(u'Then conference room (.*) is displayed in the list')
def then_conference_room_is_displayed_in_the_list(step, name):
    assert _is_saved(name)


@step(u'Then conference room (.*) is not displayed in the list')
def then_conference_room_is_not_displayed_in_the_list(step, name):
    assert not _is_saved(name)


@step(u'When I create a conference room with name (.*) with number (\d+) with max participants (\d+)')
def when_i_create_a_conference_room_with_name_number_max_participants(step, name, confno, maxusers):
    import context_steps as ctx
    ctx.when_i_edit_a_context(step, 'default')
    ctx.when_i_edit_conference_room_ranges(step)
    ctx.when_i_add_conference_room_interval(step, 9000, 9999)
    _delete_all_meetme()
    _open_add_form()
    _type_name(name)
    _type_context('default')
    _type_confno(confno)
    _type_maxusers(maxusers)
    submit_form()
