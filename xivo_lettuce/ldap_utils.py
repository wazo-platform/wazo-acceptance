# -*- coding: utf-8 -*-
#
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

import ldap.modlist
import time

from xivo_lettuce.ssh import SSHClient
from lettuce import world

LDAP_SSH_HOSTNAME = 'openldap-dev.lan-quebec.avencall.com'
LDAP_SSH_LOGIN = 'root'
LDAP_URI = 'ldap://openldap-dev.lan-quebec.avencall.com:389/'
LDAP_LOGIN = 'cn=admin,dc=lan-quebec,dc=avencall,dc=com'
LDAP_PASSWORD = 'superpass'
LDAP_USER_GROUP = 'ou=people,dc=lan-quebec,dc=avencall,dc=com'


def sanitize_string(text):
    if isinstance(text, unicode):
        text = text.encode('utf-8')
    return text


def escape_ldap_string(text):
    return text.replace('\\', '\\\\')


def encode_entry(entry):
    return dict((key, sanitize_string(value)) for key, value in entry.iteritems())


def add_or_replace_entry(entry):
    entry = encode_entry(entry)
    ldap_server = connect_to_server()

    common_name = entry['cn']
    dn = _get_entry_id(common_name)

    if _ldap_has_entry(ldap_server, common_name):
        delete_entry(ldap_server, common_name)
    add_entry(ldap_server, dn, entry)

    ldap_server.unbind_s()


def connect_to_server():
    ldap_server = ldap.initialize(LDAP_URI)
    ldap_server.simple_bind(LDAP_LOGIN, LDAP_PASSWORD)
    return ldap_server


def _ldap_has_entry(ldap_server, common_name):
    cn = escape_ldap_string(common_name)
    ldap_results = ldap_server.search_s(LDAP_USER_GROUP, ldap.SCOPE_SUBTREE, '(cn=%s)' % cn)
    if ldap_results:
        return True
    else:
        return False


def delete_entry(ldap_server, common_name):
    entry_id = _get_entry_id(common_name)
    ldap_server.delete_s(entry_id)


def _get_entry_id(common_name):
    cn = escape_ldap_string(common_name)
    return 'cn=%s,%s' % (cn, LDAP_USER_GROUP)


def add_entry(ldap_server, dn, entry):
    entry_encoded = ldap.modlist.addModlist(entry)
    ldap_server.add_s(dn, entry_encoded)


def start_ldap_server():
    ssh_client = SSHClient(LDAP_SSH_HOSTNAME, LDAP_SSH_LOGIN)
    cmd = ['service', 'slapd', 'start']
    ssh_client.check_call(cmd)


def stop_ldap_server():
    ssh_client = SSHClient(LDAP_SSH_HOSTNAME, LDAP_SSH_LOGIN)
    cmd = ['service', 'slapd', 'stop']
    ssh_client.check_call(cmd)


def _kvm_ssh_client():
    ssh_client = SSHClient(world.config.kvm_hostname, world.config.kvm_login)

    return ssh_client


def shutdown_ldap_server():
    ssh_client = _kvm_ssh_client()

    cmd = ['virsh', 'shutdown', world.config.kvm_vm_name]
    ssh_client.check_call(cmd)
    time.sleep(world.config.shutdown_timeout)


def boot_ldap_server():
    ssh_client = _kvm_ssh_client()

    cmd = ['virsh', 'start', world.config.kvm_vm_name]
    ssh_client.check_call(cmd)
    time.sleep(world.config.kvm_boot_timeout)


def is_ldap_booted():
    ssh_client = _kvm_ssh_client()

    cmd = ['virsh', 'list']

    output = ssh_client.out_call(cmd)
    for line in output.split('\n'):
        if world.config.kvm_vm_name in line:
            return True

    return False
