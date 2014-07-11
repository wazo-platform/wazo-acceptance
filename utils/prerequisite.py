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

import subprocess

from lettuce import world

from xivo_acceptance.helpers import context_helper
from xivo_dao.helpers import db_manager
from xivo_lettuce import common, assets
from xivo_lettuce.assets import copy_asset_to_server
from xivo_lettuce.terrain import initialize, deinitialize


def main():
    print 'Initializing ...'
    initialize()
    try:
        print 'Configuring WebService Access on XiVO'
        _create_webservices_access()

        print 'Configuring PostgreSQL on XiVO'
        _create_pgpass_on_remote_host()
        _allow_remote_access_to_pgsql()

        print 'Configuring RabbitMQ on XiVO'
        _allow_remote_access_to_rabbitmq()

        print 'Configuring Provd REST API on XiVO'
        _allow_provd_listen_on_all_interfaces()

        print 'Installing packages'
        _install_packages(['tcpflow'])

        print 'Installing chan_test (module for asterisk)'
        _install_chan_test()

        print 'Adding context'
        context_helper.update_contextnumbers_queue('statscenter', 5000, 5100)
        context_helper.update_contextnumbers_user('statscenter', 1000, 1100)
        context_helper.update_contextnumbers_user('default', 1000, 1999)
        context_helper.update_contextnumbers_group('default', 2000, 2999)
        context_helper.update_contextnumbers_queue('default', 3000, 3999)
        context_helper.update_contextnumbers_meetme('default', 4000, 4999)
        context_helper.update_contextnumbers_incall('from-extern', 1000, 4999, 4)

        print 'Restarting All XiVO Services'
        _xivo_service_restart_all()
    finally:
        deinitialize()


def _create_webservices_access():
    copy_asset_to_server('webservices.sql', '/tmp')
    cmd = ['sudo', '-u', 'postgres', 'psql', '-f', '/tmp/webservices.sql']
    world.ssh_client_xivo.check_call(cmd)


def _create_pgpass_on_remote_host():
    cmd = ['echo', '*:*:asterisk:asterisk:proformatique', '>', '.pgpass']
    world.ssh_client_xivo.check_call(cmd)
    cmd = ['chmod', '600', '.pgpass']
    world.ssh_client_xivo.check_call(cmd)


def _allow_remote_access_to_pgsql():
    hba_file = '/etc/postgresql/9.1/main/pg_hba.conf'
    postgres_conf_file = '/etc/postgresql/9.1/main/postgresql.conf'

    _add_line_to_remote_file('host all all 192.168.32.0/24 md5', hba_file)
    _add_line_to_remote_file('host all all 10.0.0.0/8 md5', hba_file)
    _add_line_to_remote_file("listen_addresses = '*'", postgres_conf_file)

    command = ['service', 'postgresql', 'restart']
    world.ssh_client_xivo.check_call(command)
    db_manager.reinit()


def _allow_remote_access_to_rabbitmq():
    line_to_remove = "tcp_listeners"
    _remove_line_from_remote_file(line_to_remove, '/etc/rabbitmq/rabbitmq.config')


def _add_line_to_remote_file(line_text, file_name):
    command = ['grep', '-F', '"%s"' % line_text, file_name, '||', '$(echo "%s" >> %s)' % (line_text, file_name)]
    world.ssh_client_xivo.check_call(command)


def _remove_line_from_remote_file(line_text, file_name):
    command = ['sed', '-i', '-e', '/%s/d' % line_text, file_name]
    world.ssh_client_xivo.check_call(command)


def _xivo_service_restart_all():
    command = ['xivo-service', 'restart', 'all']
    world.ssh_client_xivo.check_call(command)


def _allow_provd_listen_on_all_interfaces():
    query = 'UPDATE provisioning SET net4_ip_rest = \'0.0.0.0\''
    world.config.dao_engine.execute(query)
    common.open_url('commonconf')


def _install_packages(packages):
    command = ['apt-get', 'update', '&&', 'apt-get', 'install', '-y']
    command.extend(packages)
    world.ssh_client_xivo.check_call(command)


def _install_chan_test():
    asset_full_path = assets.full_path('chan_test.so')
    remote_path = '/usr/lib/asterisk/modules/chan_test.so'
    command = ['scp', asset_full_path, '%s:%s' % (world.config.xivo_host, remote_path)]
    subprocess.call(command)


if __name__ == '__main__':
    main()
