# -*- coding: utf-8 -*-
# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step
from hamcrest import assert_that, equal_to
from xivo_acceptance.helpers import cti_helper


@step(u'(?:Given|When) I enable DND on XiVO Client')
def when_i_set_enable_on_xivo_client(step):
    cti_helper.set_dnd(True)


@step(u'(?:Given|When) I disable DND on XiVO Client')
def when_i_disable_dnd_on_xivo_client(step):
    cti_helper.set_dnd(False)


@step(u'Then the DND is enabled on XiVO Client')
def then_the_dnd_is_enabled_on_xivo_client(step):
    enabled = cti_helper.get_dnd()['enabled']
    assert_that(enabled, equal_to(True))


@step(u'Then the DND is disabled on XiVO Client')
def then_the_dnd_is_disabled_on_xivo_client(step):
    enabled = cti_helper.get_dnd()['enabled']
    assert_that(enabled, equal_to(False))


@step(u'(?:Given|When) I enable incoming call filtering on XiVO Client')
def when_i_enable_incallfilter_on_xivo_client(step):
    cti_helper.set_incallfilter(True)


@step(u'(?:Given|When) I disable incoming call filtering on XiVO Client')
def when_i_disable_incallfilter_on_xivo_client(step):
    cti_helper.set_incallfilter(False)


@step(u'Then the incoming call filtering is enabled on XiVO Client')
def then_the_incoming_call_filtering_is_enabled_on_xivo_client(step):
    enabled = cti_helper.get_incallfilter()['enabled']
    assert_that(enabled, equal_to(True))


@step(u'Then the incoming call filtering is disabled on XiVO Client')
def then_the_incoming_call_filtering_is_disabled_on_xivo_client(step):
    enabled = cti_helper.get_incallfilter()['enabled']
    assert_that(enabled, equal_to(False))


@step(u'(?:Given|When) I enable forwarding on no-answer with destination "([^"]*)" on XiVO Client')
def when_i_enable_forwarding_on_noanswer_on_xivo_client(step, destination):
    cti_helper.set_noanswer(True, destination)


@step(u'Then the forwarding on no-answer is disabled on XiVO Client')
def then_the_forwarding_on_noanswer_is_enabled_on_xivo_client(step):
    enabled = cti_helper.get_incallfilter()['enabled']
    assert_that(enabled, equal_to(False))


@step(u'Then the forwarding on no-answer is enabled with destination "([^"]*)" on XiVO Client')
def then_the_forwarding_on_noanswer_is_disabled_with_destination_on_xivo_client(step, expected_destination):
    enabled = cti_helper.get_noanswer()['enabled']
    destination = cti_helper.get_noanswer()['destination']
    assert_that(enabled, equal_to(True))
    assert_that(destination, equal_to(expected_destination))


@step(u'(?:Given|When) I enable forwarding on busy with destination "([^"]*)" on XiVO Client')
def when_i_enable_forwarding_on_busy_on_xivo_client(step, destination):
    cti_helper.set_busy(True, destination)


@step(u'Then the forwarding on busy is disabled on XiVO Client')
def then_the_forwarding_on_busy_is_disabled_on_xivo_client(step):
    enabled = cti_helper.get_busy()['enabled']
    assert_that(enabled, equal_to(False))


@step(u'Then the forwarding on busy is enabled with destination "([^"]*)" on XiVO Client')
def then_the_forwarding_on_noanswer_is_enabled_with_destination_on_xivo_client(step, expected_destination):
    enabled = cti_helper.get_busy()['enabled']
    destination = cti_helper.get_busy()['destination']
    assert_that(enabled, equal_to(True))
    assert_that(destination, equal_to(expected_destination))


@step(u'(?:Given|When) I enable unconditional forwarding with destination "([^"]*)" on XiVO Client')
def when_i_enable_unconditional_forwarding_on_xivo_client(step, destination):
    cti_helper.set_unconditional(True, destination)


@step(u'Then the unconditional forwarding is disabled on XiVO Client')
def then_the_unconditional_forwarding_is_disabled_on_xivo_client(step):
    enabled = cti_helper.get_unconditional()['enabled']
    assert_that(enabled, equal_to(False))


@step(u'Then the unconditional forwarding is enabled with destination "([^"]*)" on XiVO Client')
def then_the_unconditional_forwarding_is_enabled_with_destination_on_xivo_client(step, expected_destination):
    enabled = cti_helper.get_unconditional()['enabled']
    destination = cti_helper.get_unconditional()['destination']
    assert_that(enabled, equal_to(True))
    assert_that(destination, equal_to(expected_destination))


@step(u'(?:Given|When) I disable all forwards on XiVO Client')
def when_i_disable_all_forwards_on_xivo_client(step):
    cti_helper.disable_all_forwards()


@step(u'Then the disable all forwards is enabled on XiVO Client')
def then_the_disable_all_forwards_is_disabled_on_xivo_client(step):
    enabled = cti_helper.get_disable_all_forwards()['enabled']
    assert_that(enabled, equal_to(True))
