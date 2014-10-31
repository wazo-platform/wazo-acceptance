#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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

import sys

from lettuce import world

from xivo_acceptance.config import XivoAcceptanceConfig, load_config
from xivo_acceptance.helpers import line_helper, context_helper, \
    trunkcustom_helper
from xivo_acceptance.helpers import user_line_extension_helper as ule_helper
from xivo_acceptance.lettuce import terrain
from xivo_acceptance.service import prerequisite
from xivo_ws.destination import UserDestination
from xivo_ws.objects.incall import Incall
from xivo_ws.objects.outcall import Outcall, OutcallExten


def main(args):
    if not args:
        print 'Usage: %s xivo_host' % sys.argv[0]
        sys.exit()

    xivo_host = args[0]

    print 'Initializing...'
    world.config = load_config()
    world.config['xivo_host'] = xivo_host
    world.xivo_acceptance_config = XivoAcceptanceConfig(world.config)
    terrain._setup_ssh_client()
    terrain._setup_ws()
    terrain._setup_provd()
    terrain._setup_browser()
    PrepareXivoBiz()


class PrepareXivoBiz(object):

    def __init__(self):
        print 'Configuring prerequisites...'
        prerequisite._create_webservices_access()
        prerequisite._create_pgpass_on_remote_host()
        prerequisite._allow_remote_access_to_pgsql()
        prerequisite._xivo_service_restart_all()

        self._check_configuration_dahdi()
        self._configuration_dahdi()

        self._prepare_context()
        self._prepare_trunk()
        self._prepare_user()
        self._prepare_outcall()
        self._prepare_incall()

        print 'Configuration finished.'

    def _prepare_context(self):
        print 'Configuring Context..'
        context_helper.update_contextnumbers_user('default', 100, 199)
        context_helper.update_contextnumbers_incall('from-extern', 1000, 2000, 4)

    def _prepare_trunk(self):
        print 'Configuring Trunk..'
        data1 = {
            'name': 'dahdi-g1',
            'interface': 'dahdi/g1'
        }
        trunkcustom_helper.add_or_replace_trunkcustom(data1)

    def _prepare_user(self):
        print 'Configuring User..'
        user_data_tpl = {
            'firstname': 'user',
            'line_context': 'default',
            'enable_client': True,
            'client_password': '12345',
            'client_profile': 'Client'
        }
        user1_data = {
            'lastname': '1',
            'line_number': '101',
            'client_username': 'user1'
        }
        user1_data.update(user_data_tpl)
        self._user1_id = ule_helper.add_or_replace_user(user1_data)
        user2_data = {
            'lastname': '2',
            'line_number': '102',
            'client_username': 'user2'
        }
        user2_data.update(user_data_tpl)
        self._user2_id = ule_helper.add_or_replace_user(user2_data)

        self._line1 = line_helper.find_with_exten_context('101', 'default')
        self._line2 = line_helper.find_with_exten_context('102', 'default')

        print
        print 'User1 infos:'
        print 'Name (line): %s' % self._line1.name
        print 'Secret (line): %s' % self._line1.secret
        print 'Username: %s' % user1_data['client_username']
        print 'Password: %s' % user1_data['client_password']
        print
        print 'User2 infos:'
        print 'Name (line): %s' % self._line2.name
        print 'Secret (line): %s' % self._line2.secret
        print 'Username: %s' % user2_data['client_username']
        print 'Password: %s' % user2_data['client_password']
        print

    def _prepare_incall(self):
        print 'Configuring Incall..'
        incall_exist = world.ws.incalls.search('1001')
        if not incall_exist:
            incall = Incall()
            incall.number = '1001'
            incall.context = 'from-extern'
            incall.destination = UserDestination(self._user1_id)
            world.ws.incalls.add(incall)
        incall_exist = world.ws.incalls.search('1002')
        if not incall_exist:
            incall = Incall()
            incall.number = '1002'
            incall.context = 'from-extern'
            incall.destination = UserDestination(self._user2_id)
            world.ws.incalls.add(incall)

    def _prepare_outcall(self):
        print 'Configuring Outcall..'
        outcall_exist = world.ws.outcalls.search('to_dahdi')
        if not outcall_exist:
            outcall = Outcall()
            outcall.name = 'to_dahdi'
            outcall.context = 'to-extern'
            outcall.trunks = [trunkcustom_helper.find_trunkcustom_id_with_name('dahdi-g1')]
            outcall.extens = [OutcallExten(exten='6XXXX', stripnum=1)]
            world.ws.outcalls.add(outcall)

    def _configuration_dahdi(self):
        print 'Configuring Dahdi..'
        cmd = ['dahdi_genconf']
        world.ssh_client_xivo.check_call(cmd)
        cmd = ['sed', '-i', '"s/,crc4//g"', '/etc/dahdi/system.conf']
        world.ssh_client_xivo.check_call(cmd)
        cmd = ['sed', '-i', '"s/group=0,11/group=1/g"', '/etc/asterisk/dahdi-channels.conf']
        world.ssh_client_xivo.check_call(cmd)
        cmd = ['sed', '-i', '"s/group=0,12/group=2/g"', '/etc/asterisk/dahdi-channels.conf']
        world.ssh_client_xivo.check_call(cmd)
        cmd = ['sed', '-i', '"s/context = default//g"', '/etc/asterisk/dahdi-channels.conf']
        world.ssh_client_xivo.check_call(cmd)
        cmd = ['sed', '-i', '"s/group = 63//g"', '/etc/asterisk/dahdi-channels.conf']
        world.ssh_client_xivo.check_call(cmd)
        cmd = ['sed', '-i', '"23s/pri_cpe/pri_net/"', '/etc/asterisk/dahdi-channels.conf']
        world.ssh_client_xivo.check_call(cmd)
        cmd = ['xivo-service', 'restart']
        print 'Wait during xivo-service restart'
        world.ssh_client_xivo.check_call(cmd)
        cmd = ['asterisk', '-rx', '"dahdi show status"']
        res = world.ssh_client_xivo.out_call(cmd)
        print 'result of "dahdi show status": %s' % res

    def _check_configuration_dahdi(self):
        cmd = ['lspci', '|', 'grep', 'Digium']
        world.ssh_client_xivo.check_call(cmd)


if __name__ == '__main__':
    main(sys.argv[1:])
