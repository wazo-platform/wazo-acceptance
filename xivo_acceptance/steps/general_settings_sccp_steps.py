# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from lettuce import step

from xivo_acceptance.helpers import sccp_helper
from xivo_acceptance.lettuce import common, form
from xivo_acceptance.lettuce.form import submit
from xivo_acceptance.lettuce.form.checkbox import Checkbox
from xivo_acceptance.lettuce.widget.codec import CodecWidget


@step(u'Given the SCCP directmedia is disabled')
def given_the_sccp_directmedia_is_disabled(step):
    sccp_helper.disable_directmedia()


@step(u'Given the SCCP dial timeout is at "(\d+)" seconds')
def given_the_sccp_dial_timeout_is_at_1_seconds(step, timeout):
    sccp_helper.set_dialtimeout(timeout)


@step(u'Given the SCCP language is "([^"]*)"')
def given_the_sccp_language_is_1(step, language):
    sccp_helper.set_language(language)


@step(u'When I enable the SCCP directmedia')
def when_i_enable_the_sccp_directmedia(step):
    common.open_url('sccpgeneralsettings')
    directmedia_checkbox = Checkbox.from_id("it-sccpgeneralsettings-directmedia")
    directmedia_checkbox.check()
    form.submit.submit_form()


@step(u'When I disable the SCCP directmedia')
def when_i_disable_the_sccp_directmedia(step):
    common.open_url('sccpgeneralsettings')
    directmedia_checkbox = Checkbox.from_id("it-sccpgeneralsettings-directmedia")
    directmedia_checkbox.uncheck()
    submit.submit_form()


@step(u'When I change the SCCP dial timeout to "([^"]*)" seconds')
def when_i_change_the_sccp_dial_timeout_to_1_seconds(step, timeout):
    common.open_url('sccpgeneralsettings')
    form.input.set_text_field_with_id('it-sccpgeneralsettings-dialtimeout', timeout)
    form.submit.submit_form()


@step(u'When I select the SCCP language "([^"]*)"')
def when_i_select_the_sccp_language_group1(step, language):
    common.open_url('sccpgeneralsettings')
    form.select.set_select_field_with_id('it-sccpgeneralsettings-language', language)
    form.submit.submit_form()


@step(u'When I customize SCCP codecs to:')
def when_i_customize_sccp_codecs_to(step):
    common.open_url('sccpgeneralsettings')
    codec_widget = CodecWidget()
    codec_widget.customize(item['codec'] for item in step.hashes)
    submit.submit_form()


@step(u'When I disable SCCP codecs customization')
def when_i_disable_sccp_codecs_customization(step):
    common.open_url('sccpgeneralsettings')
    codec_widget = CodecWidget()
    codec_widget.uncustomize()
    submit.submit_form()
