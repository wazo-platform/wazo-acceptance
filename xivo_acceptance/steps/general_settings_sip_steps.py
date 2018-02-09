# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from lettuce import step

from xivo_acceptance.lettuce import common, form
from xivo_acceptance.lettuce.form.checkbox import Checkbox


@step(u'I go on the General Settings > SIP Protocol page, tab "([^"]*)"')
def i_go_on_the_general_settings_sip_protocol_page_tab(step, tab):
    common.open_url('general_sip')
    common.go_to_tab(tab)


@step(u'When I enable the "([^"]*)" option')
def when_i_enable_the_sip_encryption_option(step, label):
    option = _get_sip_option_from_label(label)
    option.check()
    form.submit.submit_form()


@step(u'When I disable the "([^"]*)" option')
def when_i_disable_the_sip_encryption_option(step, label):
    option = _get_sip_option_from_label(label)
    option.uncheck()
    form.submit.submit_form()


def _get_sip_option_from_label(label):
    option = Checkbox.from_label(label)
    return option
