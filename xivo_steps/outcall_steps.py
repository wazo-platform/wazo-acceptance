# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import time

from hamcrest import *
from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException
from xivo_lettuce import common
from xivo_lettuce.common import edit_line, find_line, go_to_tab, open_url, \
    remove_line
from xivo_lettuce.manager.outcall_manager import exten_line
from xivo_lettuce.manager_ws import trunksip_manager_ws, outcall_manager_ws
from xivo_lettuce import form
from selenium.webdriver.support.select import Select
from xivo_lettuce.manager_ws import context_manager_ws


@step(u'Given there is no outcall "([^"]*)"$')
def given_there_is_no_outcall(step, search):
    common.remove_element_if_exist('outcall', search)


@step(u'Given there is an outcall "([^"]*)" with trunk "([^"]*)" and no extension matched')
def given_there_is_an_outcall_with_trunk_and_no_extensions_matched(step, outcall_name, trunk_name):
    trunksip_manager_ws.add_or_replace_trunksip(world.dummy_ip_address, trunk_name)
    trunk_id = trunksip_manager_ws.find_trunksip_id_with_name(trunk_name)
    data = {'name': outcall_name,
            'context': 'to-extern',
            'trunks': [trunk_id]}
    outcall_manager_ws.add_or_replace_outcall(data)


@step(u'Given there is an outcall "([^"]*)" with trunk "([^"]*)" with extension patterns')
def given_there_is_an_outcall_with_trunk_with_extension_patterns(step, outcall_name, trunk_name):
    trunksip_manager_ws.add_or_replace_trunksip(world.dummy_ip_address, trunk_name)
    trunk_id = trunksip_manager_ws.find_trunksip_id_with_name(trunk_name)

    extensions = []
    for outcall_extension in step.hashes:
        new_extension = {}
        new_extension['exten'] = outcall_extension['extension_pattern']
        new_extension['stripnum'] = outcall_extension.get('stripnum', 0)
        new_extension['caller_id'] = outcall_extension.get('caller_id', '')
        extensions.append(new_extension)

    data = {'name': outcall_name,
            'context': 'to-extern',
            'trunks': [trunk_id],
            'extens': extensions}
    outcall_manager_ws.add_or_replace_outcall(data)


@step(u'Given there is an outcall "([^"]*)" in context "([^"]*)" with trunk "([^"]*)"')
def given_there_is_an_outcall_in_context_with_trunk(step, outcall_name, outcall_context, trunk_name):
    context_manager_ws.add_or_replace_context(outcall_context, outcall_context, 'outcall')
    trunksip_manager_ws.add_or_replace_trunksip(world.dummy_ip_address, trunk_name)
    trunk_id = trunksip_manager_ws.find_trunksip_id_with_name(trunk_name)
    data = {'name': outcall_name,
            'context': outcall_context,
            'trunks': [trunk_id]}
    outcall_manager_ws.add_or_replace_outcall(data)


@step(u'Given there is no outcall "([^"]*)"')
def given_there_is_no_outcall(step, name):
    outcall_manager_ws.delete_outcalls_with_name(name)


@step(u'When I create an outcall with name "([^"]*)" and trunk "([^"]*)"')
def when_i_create_an_outcall_with_name_and_trunk(step, name, trunk):
    open_url('outcall', 'add')
    input_name = world.browser.find_element_by_id('it-outcall-name', 'Outcall form not loaded')
    input_name.send_keys(name)

    # Wait for the Javascript to fill the trunk list
    time.sleep(1)

    input_trunk = world.browser.find_element_by_xpath(
        "//div[@id='outcalltrunklist']//div[@class='available']//li[contains(@title, %s)]//a" % trunk)
    input_trunk.click()
    # Wait for the Javascript to move the trunk
    time.sleep(1)
    form.submit.submit_form()


@step(u'When i edit the outcall "([^"]*)" and set context to "([^"]*)"')
def when_i_edit_the_outcall_and_set_context(step, name, context):
    open_url('outcall', 'list')
    edit_line(name)
    type_field = Select(world.browser.find_element_by_id('it-outcall-context', 'Outcall form not loaded'))
    type_field.select_by_value(context)
    form.submit.submit_form()


@step(u'When I remove the outcall "([^"]*)"')
def when_i_remove_the_outcall(step, name):
    open_url('outcall', 'list')
    remove_line(name)


@step(u'When I remove extension patterns from outcall "([^"]*)":')
def when_i_remove_extension_patterns_from_outcall_1(step, outcall_name):
    open_url('outcall', 'list')
    edit_line(outcall_name)
    go_to_tab('Exten')

    for outcall_extension in step.hashes:
        extension_pattern = outcall_extension['extension_pattern']
        delete_button = exten_line(extension_pattern).find_element_by_id('lnk-del-row')
        delete_button.click()
        # Wait for the Javascript to remove the line
        time.sleep(1)
    form.submit.submit_form()


@step(u'When I add the following extension patterns to the outcall "([^"]*)":')
def when_i_add_the_following_extension_patterns_to_the_outcall_1(step, outcall_name):
    open_url('outcall', 'list')
    edit_line(outcall_name)
    go_to_tab('Exten')

    for outcall_extension in step.hashes:
        add_button = world.browser.find_element_by_id('lnk-add-row', 'Can\'t add an exten')
        add_button.click()
        input_exten = world.browser.find_elements_by_xpath(
            "//table[@id='list_exten']//input[@name='dialpattern[exten][]']")[-1]
        input_exten.send_keys(outcall_extension['extension_pattern'])

    form.submit.submit_form()


@step(u'Then the outcall "([^"]*)" has the extension patterns:')
def then_the_outcall_1_has_the_extension_patterns(step, outcall_name):
    open_url('outcall', 'list')
    edit_line(outcall_name)
    go_to_tab('Exten')

    for outcall_extension in step.hashes:
        extension_pattern = outcall_extension['extension_pattern']
        extension_pattern_input = exten_line(extension_pattern).find_element_by_xpath(".//input[@name='dialpattern[exten][]']")
        assert_that(extension_pattern_input, not_none())


@step(u'Then the outcall "([^"]*)" does not have extension patterns:')
def then_the_outcall_1_does_not_have_extension_patterns(step, outcall_name):
    open_url('outcall', 'list')
    edit_line(outcall_name)
    go_to_tab('Exten')

    for outcall_extension in step.hashes:
        extension_pattern = outcall_extension['extension_pattern']
        try:
            exten_line(extension_pattern)
        except NoSuchElementException:
            pass
        else:
            raise Exception('extension pattern %s unexpectedly found in outcall %s' %
                            (outcall_extension, outcall_name))


@step(u'Then there is no outcall "([^"]*)"')
def then_there_is_no_outcall(step, name):
    open_url('outcall', 'list')
    try:
        find_line(name)
    except NoSuchElementException:
        pass
    else:
        assert False


@step(u'Then there are outcalls with infos:')
def then_there_are_outcalls_with_infos(step):
    outcalls = [{u'name': outcall.name,
                 u'context': outcall.context}
                for outcall in outcall_manager_ws.list_outcalls()]
    for expected_outcall_attributes in step.hashes:
        assert_that(outcalls, has_item(has_entries(expected_outcall_attributes)))
