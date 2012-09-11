# -*- coding: utf-8 -*-

from lettuce.registry import world


def get_asterisk_conf(file, var_name):
    command = ['xivo-confgen', 'asterisk/%s' % file, '|', 'grep', var_name]
    ret = world.ssh_client_xivo.out_call(command)
    if ret:
        val = ret.split('=')[1].strip()
        return val
    assert(False)
