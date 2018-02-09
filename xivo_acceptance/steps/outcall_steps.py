# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

import time

from hamcrest import (assert_that,
                      empty,
                      is_not,
                      not_none)
from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException

from xivo_acceptance.action.webi import outcall as outcall_action_webi
from xivo_acceptance.helpers import outcall_helper, trunksip_helper
from xivo_acceptance.lettuce import common, form


@step(u'Given there is no outcall "([^"]*)"')
def given_there_is_no_outcall(step, name):
    outcall_helper.delete_outcalls_with_name(name)


@step(u'Given there is an outcall "([^"]*)" with trunk "([^"]*)" and no extension matched')
def given_there_is_an_outcall_with_trunk_and_no_extensions_matched(step, outcall_name, trunk_name):
    trunksip_helper.add_or_replace_trunksip(world.dummy_ip_address, trunk_name)
    trunk_id = trunksip_helper.find_trunksip_id_with_name(trunk_name)

    outcall = {'name': outcall_name,
               'trunks': [{'id': trunk_id}]}
    outcall_helper.add_or_replace_outcall(outcall)


@step(u'Given there is an outcall "([^"]*)" with trunk "([^"]*)" with extension patterns')
def given_there_is_an_outcall_with_trunk_with_extension_patterns(step, outcall_name, trunk_name):
    trunksip_helper.add_or_replace_trunksip(world.dummy_ip_address, trunk_name)
    trunk_id = trunksip_helper.find_trunksip_id_with_name(trunk_name)

    extensions = []
    for outcall_extension in step.hashes:
        extension = {}
        extension['context'] = 'to-extern'
        extension['exten'] = outcall_extension['extension_pattern']
        extension['stripnum'] = outcall_extension.get('stripnum', 0)
        extension['caller_id'] = outcall_extension.get('caller_id', '')
        extensions.append(extension)

    outcall = {'name': outcall_name,
               'trunks': [{'id': trunk_id}],
               'extensions': extensions}
    outcall_helper.add_or_replace_outcall(outcall)


@step(u'Given there is an outcall "([^"]*)" with trunk "([^"]*)"$')
def given_there_is_an_outcall_with_trunk(step, outcall_name, trunk_name):
    trunksip_helper.add_or_replace_trunksip(world.dummy_ip_address, trunk_name)
    trunk_id = trunksip_helper.find_trunksip_id_with_name(trunk_name)

    outcall = {'name': outcall_name,
               'trunks': [{'id': trunk_id}]}
    outcall_helper.add_or_replace_outcall(outcall)


@step(u'Then there are an outcall "([^"]*)" with preprocess subroutine "([^"]*)"')
def then_there_are_an_outcall(step, name, preprocess_subroutine):
    outcalls = world.confd_client.outcalls.list(name=name, preprocess_subroutine=preprocess_subroutine)
    assert_that(outcalls['items'], is_not(empty()))


@step(u'When I create an outcall with name "([^"]*)" and trunk "([^"]*)" in the webi')
def when_i_create_an_outcall_with_name_and_trunk_in_the_webi(step, name, trunk):
    common.open_url('outcall', 'add')
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


@step(u'When i edit the outcall "([^"]*)" and set preprocess subroutine to "([^"]*)" in the webi')
def when_i_edit_the_outcall_and_set_preprocess_subroutine_in_the_webi(step, name, preprocess_subroutine):
    common.open_url('outcall', 'list')
    common.edit_line(name)
    input_field = world.browser.find_element_by_id('it-outcall-preprocess-subroutine', 'Outcall form not loaded')
    input_field.clear()
    input_field.send_keys(preprocess_subroutine)
    form.submit.submit_form()


@step(u'When I remove the outcall "([^"]*)" in the webi')
def when_i_remove_the_outcall_in_the_webi(step, name):
    common.open_url('outcall', 'list')
    common.remove_line(name)


@step(u'When I remove extension patterns from outcall "([^"]*)" in the webi:')
def when_i_remove_extension_patterns_from_outcall_1_in_the_webi(step, outcall_name):
    common.open_url('outcall', 'list')
    common.edit_line(outcall_name)
    common.go_to_tab('Exten')

    for outcall_extension in step.hashes:
        extension_pattern = outcall_extension['extension_pattern']
        delete_button = outcall_action_webi.exten_line(extension_pattern).find_element_by_id('lnk-del-row')
        delete_button.click()
        # Wait for the Javascript to remove the line
        time.sleep(1)
    form.submit.submit_form()


@step(u'When I add the following extension patterns to the outcall "([^"]*)" in the webi:')
def when_i_add_the_following_extension_patterns_to_the_outcall_1_in_the_webi(step, outcall_name):
    common.open_url('outcall', 'list')
    common.edit_line(outcall_name)
    common.go_to_tab('Exten')

    for outcall_extension in step.hashes:
        add_button = world.browser.find_element_by_id('lnk-add-row', 'Can\'t add an exten')
        add_button.click()
        input_exten = world.browser.find_elements_by_xpath(
            "//table[@id='list_exten']//input[@name='dialpattern[exten][]']")[-1]
        input_exten.send_keys(outcall_extension['extension_pattern'])

    form.submit.submit_form()


@step(u'Then the outcall "([^"]*)" has the extension patterns in the webi:')
def then_the_outcall_1_has_the_extension_patterns_in_the_webi(step, outcall_name):
    common.open_url('outcall', 'list')
    common.edit_line(outcall_name)
    common.go_to_tab('Exten')

    for outcall_extension in step.hashes:
        extension_pattern = outcall_extension['extension_pattern']
        extension_pattern_input = outcall_action_webi.exten_line(extension_pattern).find_element_by_xpath(
            ".//input[@name='dialpattern[exten][]']"
        )
        assert_that(extension_pattern_input, not_none())


@step(u'Then the outcall "([^"]*)" does not have extension patterns in the webi:')
def then_the_outcall_1_does_not_have_extension_patterns_in_the_webi(step, outcall_name):
    common.open_url('outcall', 'list')
    common.edit_line(outcall_name)
    common.go_to_tab('Exten')

    for outcall_extension in step.hashes:
        extension_pattern = outcall_extension['extension_pattern']
        try:
            outcall_action_webi.exten_line(extension_pattern)
        except NoSuchElementException:
            pass
        else:
            raise Exception('extension pattern %s unexpectedly found in outcall %s' %
                            (outcall_extension, outcall_name))


@step(u'Then there is no outcall "([^"]*)" in the webi')
def then_there_is_no_outcall_in_the_webi(step, name):
    common.open_url('outcall', 'list')
    assert common.find_line(name) is None
