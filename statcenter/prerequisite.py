# -*- coding: UTF-8 -*-

import socket
from lettuce import world
from xivo_lettuce.manager_ws import context_manager_ws, trunksip_manager_ws
from xivo_lettuce.terrain import initialize, deinitialize


def main():
    print 'Initializing ...'
    initialize()
    try:
        print 'Adding queue extensions interval'
        context_manager_ws.update_contextnumbers_queue('statscenter', 5000, 5100)
        print 'Adding user extensions interval'
        context_manager_ws.update_contextnumbers_user('statscenter', 1000, 1100)

        callgen_ip = socket.gethostbyname(world.callgen_host)
        print 'Adding default SIP trunk'
        trunksip_manager_ws.add_or_replace_trunksip(callgen_ip, 'to_default', 'default')
        print 'Adding statscenter SIP trunk'
        trunksip_manager_ws.add_or_replace_trunksip(callgen_ip, 'to_statscenter', 'statscenter')

        print 'Configuring PostgreSQL on XiVO'
        _create_pgpass_on_remote_host()
        _allow_remote_access_to_pgsql()
    finally:
        deinitialize()


def _create_pgpass_on_remote_host():
    cmd = ['echo', '*:*:asterisk:asterisk:proformatique', '>', '.pgpass']
    world.ssh_client_xivo.check_call(cmd)
    cmd = ['chmod', '600', '.pgpass']
    world.ssh_client_xivo.check_call(cmd)


def _allow_remote_access_to_pgsql():
    hba_file = '/etc/postgresql/9.0/main/pg_hba.conf'
    postgres_conf_file = '/etc/postgresql/9.0/main/postgresql.conf'

    _add_line_to_remote_file('host all all 192.168.32.0/24 md5', hba_file)
    _add_line_to_remote_file('host all all 10.0.0.0/8 md5', hba_file)
    _add_line_to_remote_file("listen_addresses = '*'", postgres_conf_file)

    _xivo_service_restart()


def _add_line_to_remote_file(line_text, file_name):
    command = ['grep', '-F', '"%s"' % line_text, file_name, '||', '$(echo "%s" >> %s)' % (line_text, file_name)]
    world.ssh_client_xivo.check_call(command)


def _xivo_service_restart():
    command = ['xivo-service', 'restart', 'all']
    world.ssh_client_xivo.check_call(command)


if __name__ == '__main__':
    main()
