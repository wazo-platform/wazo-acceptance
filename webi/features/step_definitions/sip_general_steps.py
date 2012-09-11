# -*- coding: utf-8 -*-

from lettuce import step
from xivo_lettuce.checkbox import Checkbox
from xivo_lettuce.common import go_to_tab, open_url, submit_form
from xivo_lettuce.manager import asterisk_manager


@step(u'I go on the General Settings > SIP Protocol page, tab "([^"]*)"')
def i_go_on_the_general_settings_sip_protocol_page_tab(step, tab):
    open_url('general_sip')
    go_to_tab(tab)


@step(u'When I enable the SIP encryption option')
def when_i_enable_the_sip_encryption_option(step):
    option = _get_sip_encryption_option()
    option.check()
    submit_form()


@step(u'When I disable the SIP encryption option')
def when_i_disable_the_sip_encryption_option(step):
    option = _get_sip_encryption_option()
    option.uncheck()
    submit_form()


@step(u'Then the SIP encryption option is enabled')
def then_the_sip_encryption_option_is_enabled(step):
    option = _get_sip_encryption_option()
    assert option.is_checked()


@step(u'Then the SIP encryption option is disabled')
def then_the_sip_encryption_option_is_disabled(step):
    option = _get_sip_encryption_option()
    assert not option.is_checked()


@step(u'^Then I should see "([^"]*)" to "([^"]*)" in "([^"]*)"$')
def then_i_see_sip_encryption_in_file(step, var_name, expected_var_val, file):
    var_val = asterisk_manager.get_asterisk_conf(file, var_name)
    assert(expected_var_val == var_val)


def _get_sip_encryption_option():
    open_url('general_sip')
    go_to_tab('Security')
    option = Checkbox.from_label('Encryption')

    return option
