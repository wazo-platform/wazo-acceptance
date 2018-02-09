# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from lettuce import step
from selenium.common.exceptions import NoSuchElementException

from xivo_acceptance.action.webi import general_settings_iax as general_settings_iax_action_webi
from xivo_acceptance.lettuce import form, common
from xivo_acceptance.lettuce.form.checkbox import Checkbox


@step(u'Given the IAX call limit to "([^"]*)" netmask "([^"]*)" does not exist')
def given_the_iax_call_limit_to_1_netmask_2_does_not_exist(step, destination, netmask):
    general_settings_iax_action_webi.remove_call_limit_if_exists(destination, netmask)


@step(u'When I add IAX call limits with errors:')
def when_i_add_iax_call_limit_with_errors(step):
    _go_to_call_limits_form()
    _type_call_limits(step.hashes)
    form.submit.submit_form_with_errors()


@step(u'When I remove IAX call limits:')
def when_i_remove_iax_call_limits(step):
    call_limits_to_remove = step.hashes
    general_settings_iax_action_webi.remove_call_limits(call_limits_to_remove)


@step(u'When I add IAX call limits:')
def when_i_add_iax_call_limit(step):
    _go_to_call_limits_form()
    _type_call_limits(step.hashes)
    form.submit.submit_form()


@step(u'Then I see IAX call limits:')
def then_i_see_iax_call_limits(step):
    expected_call_limits = step.hashes
    for expected_call_limit in expected_call_limits:
        address = expected_call_limit['address']
        netmask = expected_call_limit['netmask']
        call_count = expected_call_limit['call_count']
        general_settings_iax_action_webi.find_call_limit_line(address, netmask, call_count)


@step(u'Then I don\'t see IAX call limits:')
def then_i_don_t_see_iax_call_limits(step):
    unexpected_call_limits = step.hashes
    for unexpected_call_limit in unexpected_call_limits:
        address = unexpected_call_limit['address']
        netmask = unexpected_call_limit['netmask']
        call_count = unexpected_call_limit['call_count']
        try:
            general_settings_iax_action_webi.find_call_limit_line(address, netmask, call_count)
        except NoSuchElementException:
            pass
        else:
            raise Exception('Call limit %s should not be visible' % unexpected_call_limit)


@step(u'Given the SRV lookup option is disabled')
def given_the_srv_lookup_option_is_disabled(step):
    option = _get_srv_lookup_option()

    if option.is_checked():
        option.uncheck()
        form.submit.submit_form()

        option = _get_srv_lookup_option()
        assert not option.is_checked()


@step(u'When I enable the SRV lookup option')
def when_i_enable_the_srv_lookup_option(step):
    option = _get_srv_lookup_option()
    option.check()
    form.submit.submit_form()


@step(u'Then the SRV lookup option is enabled')
def then_the_srv_lookup_option_is_enabled(step):
    option = _get_srv_lookup_option()
    assert option.is_checked()


@step(u'When I disable the SRV lookup option')
def when_i_disable_the_srv_lookup_option(step):
    option = _get_srv_lookup_option()
    option.uncheck()
    form.submit.submit_form()


@step(u'Then the SRV lookup option is disabled')
def then_the_srv_lookup_option_is_disabled(step):
    option = _get_srv_lookup_option()
    assert not option.is_checked()


@step(u'Given the Shrink caller ID option is disabled')
def given_the_shrink_caller_id_option_is_disabled(step):
    option = _get_shrink_caller_id_option()

    if option.is_checked():
        option.uncheck()
        form.submit.submit_form()

        option = _get_shrink_caller_id_option()
        assert not option.is_checked()


@step(u'When I enable the Shrink caller ID option')
def when_i_enable_the_shrink_caller_id_option(step):
    option = _get_shrink_caller_id_option()
    option.check()
    form.submit.submit_form()


@step(u'Then the Shrink caller ID option is enabled')
def then_the_shrink_caller_id_option_is_enabled(step):
    option = _get_shrink_caller_id_option()
    assert option.is_checked()


@step(u'When I disable the Shrink caller ID option')
def when_i_disable_the_shrink_caller_id_option(step):
    option = _get_shrink_caller_id_option()
    option.uncheck()
    form.submit.submit_form()


@step(u'Then the Shrink caller ID option is disabled')
def then_the_shrink_caller_id_option_is_disabled(step):
    option = _get_shrink_caller_id_option()
    assert not option.is_checked()


def _get_srv_lookup_option():
    common.open_url('general_iax')
    common.go_to_tab('Default')
    option = Checkbox.from_label('SRV lookup')

    return option


def _get_shrink_caller_id_option():
    common.open_url('general_iax')
    common.go_to_tab('Advanced')
    option = Checkbox.from_label('Shrink CallerID')

    return option


def _go_to_call_limits_form():
    common.open_url('general_iax')
    common.go_to_tab('Call limits')


def _type_call_limits(call_limits_config):
    for call_limit in call_limits_config:
        general_settings_iax_action_webi.type_iax_call_limit(call_limit)
