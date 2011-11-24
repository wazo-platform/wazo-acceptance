# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

from common.common import submit_form

CONTEXT_URL = '/service/ipbx/index.php/system_management/context/%s'

@step(u'When I edit a context (.*)')
def when_i_edit_a_context(step, context_name):
    URL = CONTEXT_URL % '?act=edit&id=%s'
    world.browser.get('%s%s' % (world.url, URL % context_name))
    world.browser.find_element_by_id('fd-context-name', 'Context page not loaded')
    world.context = context_name


@step(u'When I edit group ranges')
def when_i_edit_group_ranges(step):
    group = world.browser.find_element_by_xpath("//li[@id='dwsm-tab-3']//a[@href='#group']")
    group.click()
    world.browser.find_element_by_id('sb-part-group', 'Group tab not loaded')


@step(u'When I add group interval from (.*) to (.*)')
def when_i_add_group_interval(step, start, end):
    world.browser.find_element_by_id('sb-part-group', 'Group range config not loaded')
    add_button = world.browser.find_element_by_xpath("//div[@id='sb-part-group']//a[@id='add_line_button']")
    add_button.click()
    world.browser.find_element_by_id('contextnumbers-group', 'Group line not shown')
    start_field = world.browser.find_elements_by_xpath("//tbody[@id='contextnumbers-group']//input[@name='contextnumbers[group][numberbeg][]']")[-1]
    start_field.clear()
    start_field.send_keys(start)
    end_field = world.browser.find_elements_by_xpath("//tbody[@id='contextnumbers-group']//input[@name='contextnumbers[group][numberend][]']")[-1]
    end_field.clear()
    end_field.send_keys(end)
    submit_form()


@step(u'When I edit conference room ranges')
def when_i_edit_conference_room_ranges(step):
    group = world.browser.find_element_by_xpath("//li[@id='dwsm-tab-5']//a[@href='#meetme']")
    group.click()
    world.browser.find_element_by_id('sb-part-meetme', 'meetme tab not loaded')


@step(u'When I add conference room interval from (.*) to (.*)')
def when_i_add_conference_room_interval(step, start, end):
    world.browser.find_element_by_id('sb-part-meetme', 'Meetme range config not loaded')
    add_button = world.browser.find_element_by_xpath("//div[@id='sb-part-meetme']//a[@id='add_line_button']")
    add_button.click()
    world.browser.find_element_by_id('contextnumbers-meetme', 'Meetme line not shown')
    start_field = world.browser.find_elements_by_xpath("//tbody[@id='contextnumbers-meetme']//input[@name='contextnumbers[meetme][numberbeg][]']")[-1]
    start_field.clear()
    start_field.send_keys(start)
    end_field = world.browser.find_elements_by_xpath("//tbody[@id='contextnumbers-meetme']//input[@name='contextnumbers[meetme][numberend][]']")[-1]
    end_field.clear()
    end_field.send_keys(end)
    submit_form()


@step(u'Then I should see the group (.*) in context (.*) with range (.*) to (.*)')
def then_i_should_see_the_group(step, group_name, context_name, start, end):
    URL = CONTEXT_URL % '?act=edit&id=%s#group'
    world.browser.get('%s%s' % (world.url, URL % context_name))
    assert start in world.browser.page_source
    assert end in world.browser.page_source


@step(u'When I edit incall ranges')
def when_i_edit_incall_ranges(step):
    world.browser.find_element_by_id('dwsm-tab-6', 'Incall tab not loaded')
    group = world.browser.find_element_by_xpath("//li[@id='dwsm-tab-6']//a[@href='#last']")
    group.click()
    world.browser.find_element_by_id('sb-part-last', 'Incall tab not loaded')


@step(u'When I add incall interval from (.*) to (.*) with ([0-9]+) numbers')
def when_i_add_incall_interval(step, start, end, did_length):
    world.browser.find_element_by_id('sb-part-last', 'Context range page not loaded')
    add_button = world.browser.find_element_by_xpath("//div[@id='sb-part-last']//a[@id='add_line_button']")
    add_button.click()
    world.browser.find_element_by_id('contextnumbers-incall', 'Incall line not shown')

    # Do not erase the first line, so select the last one with find_elements...()[-1]
    start_field = world.browser.find_elements_by_xpath("//tbody[@id='contextnumbers-incall']//input[@name='contextnumbers[incall][numberbeg][]']")[-1]
    start_field.clear()
    start_field.send_keys(start)
    end_field = world.browser.find_elements_by_xpath("//tbody[@id='contextnumbers-incall']//input[@name='contextnumbers[incall][numberend][]']")[-1]
    end_field.clear()
    end_field.send_keys(end)
    # Don't know why the disabled select is included in the list, so compensate with a [-2]
    did_length_select = world.browser.find_elements_by_xpath('//select[@name="contextnumbers[incall][didlength][]"]//option[@value="%s"]' % did_length)[-2]
    did_length_select.click()
    world.dump_current_page()
    submit_form()
