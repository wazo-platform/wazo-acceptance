# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later
from lettuce.decorators import step
from lettuce.registry import world
from hamcrest.core import assert_that
from xivo_acceptance.lettuce import logs
from hamcrest.library.collection.issequence_containing import has_item
from hamcrest.library.text.stringcontains import contains_string


@step(u'Given live reload is enabled')
def given_live_reload_is_enabled(step):
    world.confd_client.configuration.live_reload.update({'enabled': True})


@step(u'Given live reload is disabled')
def given_live_reload_is_disabled(step):
    world.confd_client.configuration.live_reload.update({'enabled': False})


@step(u'When I enable the live reload')
def when_i_enable_the_live_reload(step):
    world.confd_client.configuration.live_reload.update({'enabled': True})


@step(u'When I disable the live reload')
def when_i_disable_the_live_reload(step):
    world.confd_client.configuration.live_reload.update({'enabled': False})


@step(u'Then the CTI is notified for a configuration change')
def then_the_cti_is_notified_for_a_configuration_change(step):
    expression = "xivo[cticonfig,update]"
    log_lines = logs.find_line_in_xivo_sysconfd_log()
    assert_that(log_lines, has_item(contains_string(expression)))
