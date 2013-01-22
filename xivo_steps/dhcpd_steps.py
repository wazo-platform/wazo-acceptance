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

from lettuce import step
from xivo_lettuce import form, sysutils
from xivo_lettuce.terrain import _webi_configured
from xivo_lettuce.manager import dhcpd_manager, commonconf_manager
from xivo_lettuce.common import open_url
from xivo_lettuce.form.checkbox import Checkbox


@step(u'When I wizard correctly executed')
def when_i_wizard_correctly_executed(step):
    assert _webi_configured()


@step(u'When I activate dhcpd server')
def when_i_activate_dhcpd_server(step):
    open_url('dhcp')
    Checkbox.from_id('it-active').check()
    dhcpd_manager.type_pool_start_end('192.168.32.20', '192.168.32.21')
    form.submit.submit_form()
    commonconf_manager.webi_exec_commonconf()


@step(u'When I desactivate dhcpd server')
def when_i_desactivate_dhcpd_server(step):
    open_url('dhcp')
    Checkbox.from_id('it-active').uncheck()
    form.submit.submit_form()
    commonconf_manager.webi_exec_commonconf()


@step(u'Then I see "([^"]*)" monitored by monit')
def then_i_see_process_monitored_by_monit(step, process_name):
    assert dhcpd_manager.process_monitored(process_name)


@step(u'Then I not see "([^"]*)" monitored by monit')
def then_i_not_see_process_monitored_by_monit(step, process_name):
    assert not dhcpd_manager.process_monitored(process_name)


@step(u'Then directory of the dhcpd update not empty')
def then_directory_at_the_dhcpd_update_not_empty(step):
    DHCPD_UPDATE_DIR = '/etc/dhcp/dhcpd_update'
    assert not sysutils.dir_is_empty(DHCPD_UPDATE_DIR)
