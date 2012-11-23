# -*- coding: UTF-8 -*-

from lettuce import world


def exec_sql_request(pg_command):
    command = ['psql', '-h', 'localhost', '-U', 'asterisk', '-c', pg_command]
    world.ssh_client_xivo.check_call(command)


def exec_sql_request_with_return(pg_command):
    command = ['psql', '-h', 'localhost', '-U', 'asterisk', '-c', pg_command]
    return world.ssh_client_xivo.out_call(command)
