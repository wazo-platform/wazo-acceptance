# -*- coding: utf-8 -*-

from lettuce import step, world
from selenium.common.exceptions import NoSuchElementException
from xivo_lettuce.common import find_line, open_url, remove_all_elements, \
    remove_line
from xivo_lettuce.manager_ws import line_manager_ws
from xivo_lettuce.manager import line_manager


@step(u'Given there is no custom lines')
def given_there_is_no_custom_lines(step):
    remove_all_elements('line', 'Customized')


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


@step(u'When I edit the line "([^"]*)"')
def when_i_edit_the_line_1(step, linenumber):
    line_ids = line_manager_ws.find_line_id_with_number(linenumber, 'default')
    if line_ids:
        open_url('line', 'edit', {'id': line_ids[0]})


@step(u'Then this line is displayed in the list')
def then_this_line_is_displayed_in_the_list(step):
    open_url('line', 'search', {'search': world.id})
    assert find_line(world.id) is not None
    open_url('line', 'search', {'search': ''})


@step(u'Then this line is not displayed in the list')
def then_this_line_is_not_displayed_in_the_list(step):
    try:
        find_line(world.id)
    except NoSuchElementException:
        pass
    else:
        assert False


@step(u'Then I see the line "([^"]*)" has its call limit to "([^"]*)"')
def then_i_see_the_line_1_has_its_call_limit_to_2(step, line_number, call_limit):
    line_id = line_manager_ws.find_line_id_with_number(line_number, 'default')[0]
    open_url('line', 'edit', {'id': line_id})

    expected_var_val = line_manager.get_value_from_ipbx_infos_tab('call_limit')
    assert expected_var_val == call_limit


@step(u'^Then I see in IPBX Infos tab value "([^"]*)" has set to (.*)$')
def then_i_see_the_value_has_set_to(step, var_name, var_val):
    expected_var_val = line_manager.get_value_from_ipbx_infos_tab(var_name)
    assert expected_var_val == var_val
