# -*- coding: UTF-8 -*-

import socket
import xivo_ws

from xivo_lettuce.terrain import _read_config
from xivo_ws.objects.siptrunk import SIPTrunk
from xivo_lettuce.manager.context_manager import add_contextnumbers_queue, \
    add_contextnumbers_user
from xivo_lettuce.ssh import SSHClient


def main():
    config = _read_config()
    Prerequisite(config)


class Prerequisite(object):

    def __init__(self, config):
        jenkins_hostname = config.get('jenkins', 'hostname')
        hostname = config.get('general', 'hostname')
        login = config.get('webservices_infos', 'login')
        password = config.get('webservices_infos', 'password')
        self.ws = xivo_ws.XivoServer(hostname, login, password)

        add_contextnumbers_queue('statscenter', 5000, 5100)
        add_contextnumbers_user('statscenter', 1000, 1100)

        local_ip = socket.gethostbyname(jenkins_hostname)
        self.add_trunksip(local_ip, 'to_default', 'default')
        self.add_trunksip(local_ip, 'to_statscenter', 'statscenter')

        self._setup_ssh_client(config)

    def add_trunksip(self, host, name, context):
        if self.has_trunksip(name):
            return
        sip_trunk = SIPTrunk()
        sip_trunk.name = name
        sip_trunk.username = sip_trunk.name
        sip_trunk.secret = sip_trunk.name
        sip_trunk.context = context
        sip_trunk.host = host
        sip_trunk.type = 'friend'
        self.ws.sip_trunk.add(sip_trunk)

    def has_trunksip(self, name):
        return self.ws.sip_trunk.search(name)

    def _setup_ssh_client(self, config):
        hostname = config.get('general', 'hostname')
        login = config.get('ssh_infos', 'login')
        ssh_client = SSHClient(hostname, login)
        self._create_pgpass_on_remote_host(ssh_client)

    def _create_pgpass_on_remote_host(self, ssh_client):
        cmd = ['echo', '*:*:asterisk:asterisk:proformatique', '>', '.pgpass']
        ssh_client.check_call(cmd)
        cmd = ['chmod', '600', '.pgpass']
        ssh_client.check_call(cmd)


if __name__ == '__main__':
    main()
