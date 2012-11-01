# -*- coding: utf-8 -*-

from lettuce import step
from xivo_lettuce import form
from xivo_lettuce.checkbox import Checkbox
from xivo_lettuce.common import go_to_tab, open_url
from xivo_lettuce.manager import asterisk_manager


@step(u'I go on the General Settings > SIP Protocol page, tab "([^"]*)"')
def i_go_on_the_general_settings_sip_protocol_page_tab(step, tab):
    open_url('general_sip')
    go_to_tab(tab)


@step(u'When I enable the "([^"]*)" option')
def when_i_enable_the_sip_encryption_option(step, label):
    option = _get_sip_option_from_label(label)
    option.check()
    form.submit_form()


@step(u'When I disable the "([^"]*)" option')
def when_i_disable_the_sip_encryption_option(step, label):
    option = _get_sip_option_from_label(label)
    option.uncheck()
    form.submit_form()


@step(u'^Then I should see "([^"]*)" to "([^"]*)" in "([^"]*)"$')
def then_i_see_sip_encryption_in_file(step, var_name, expected_var_val, file):
    var_val = asterisk_manager.get_asterisk_conf(file, var_name)
    assert(expected_var_val == var_val)


def _get_sip_option_from_label(label):
    option = Checkbox.from_label(label)

    return option
