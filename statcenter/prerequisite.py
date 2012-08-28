# -*- coding: UTF-8 -*-

import socket
from lettuce import world
from xivo_lettuce.manager import context_manager, trunksip_manager


def setup(ssh_xivo):
    context_manager.add_contextnumbers_queue('statscenter', 5000, 5100)
    context_manager.add_contextnumbers_user('statscenter', 1000, 1100)

    callgen_ip = socket.gethostbyname(world.callgen_host)
    trunksip_manager.add_or_replace_trunksip(callgen_ip, 'to_default', 'default')
    trunksip_manager.add_or_replace_trunksip(callgen_ip, 'to_statscenter', 'statscenter')

    _create_pgpass_on_remote_host(ssh_xivo)

def _create_pgpass_on_remote_host(ssh_xivo):
    cmd = ['echo', '*:*:asterisk:asterisk:proformatique', '>', '.pgpass']
    ssh_xivo.check_call(cmd)
    cmd = ['chmod', '600', '.pgpass']
    ssh_xivo.check_call(cmd)
