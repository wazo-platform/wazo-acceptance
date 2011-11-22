# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

CONTEXT_URL = 'service/ipbx/index.php/system_management/context/%s'

@step(u'When I edit a context (.*)')
def when_i_edit_a_context(step, context_name):
    URL = CONTEXT_URL % '?act=edit&id=%s'
    world.browser.get('%s%s' % (world.url, URL % context_name))
    world.wait_for_id('fd-context-name', 'Context page not loaded')
    world.context = context_name

@step(u'When I edit group ranges')
def when_i_edit_group_ranges(step):
    group = world.browser.find_element_by_xpath("//li[@id='dwsm-tab-3']//a[@href='#group']")
    group.click()
    world.wait_for_id('sb-part-group', 'Group tab not loaded')

@step(u'When I add group interval from (.*) to (.*)')
def when_i_add_group_interval(step, start, end):
    add_button = world.browser.find_element_by_xpath("//div[@id='sb-part-group']//a[@id='add_line_button']")
    add_button.click()
    world.wait_for_id('contextnumbers-group', 'Group line not shown')
    start_field = world.browser.find_elements_by_xpath("//tbody[@id='contextnumbers-group']//input[@name='contextnumbers[group][numberbeg][]']")[-1]
    start_field.clear()
    start_field.send_keys(start)
    end_field = world.browser.find_elements_by_xpath("//tbody[@id='contextnumbers-group']//input[@name='contextnumbers[group][numberend][]']")[-1]
    end_field.clear()
    end_field.send_keys(end)
    submit_button = world.browser.find_element_by_id('it-submit')
    submit_button.click()

@step(u'Then I should see the group (.*) in context (.*) with range (.*) to (.*)')
def then_i_should_see_the_group(step, group_name, context_name, start, end):
    URL = CONTEXT_URL % '?act=edit&id=%s#group'
    world.browser.get('%s%s' % (world.url, URL % context_name))
    assert start in world.browser.page_source
    assert end in world.browser.page_source
