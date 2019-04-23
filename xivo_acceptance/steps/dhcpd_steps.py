# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step
from lettuce.registry import world

from xivo_acceptance.helpers import monit_helper


@step(u'When I wizard correctly executed')
def when_i_wizard_correctly_executed(step):
    assert world.xivo_configured


@step(u'When I activate dhcpd server')
def when_i_activate_dhcpd_server(step):
    pass


@step(u'When I desactivate dhcpd server')
def when_i_desactivate_dhcpd_server(step):
    pass


@step(u'Then I see "([^"]*)" monitored by monit')
def then_i_see_process_monitored_by_monit(step, process_name):
    assert monit_helper.process_monitored(process_name)


@step(u'Then I not see "([^"]*)" monitored by monit')
def then_i_not_see_process_monitored_by_monit(step, process_name):
    assert not monit_helper.process_monitored(process_name)
