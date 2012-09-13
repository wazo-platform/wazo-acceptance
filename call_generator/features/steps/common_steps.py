# -*- coding: UTF-8 -*-

import socket

from lettuce.registry import world
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime
from utils.func import extract_number_and_context_from_extension
from lettuce.decorators import step


@step(u'Then I see rejected call to extension "([^"]+)" in asterisk log')
def then_i_see_rejected_call_in_asterisk_log(step, extension):
    number, context = extract_number_and_context_from_extension(extension)
    d = datetime.now()
    regex_date = d.strftime("%b %d %H:%M:([0-9]{2})")
    line_search = "\[%s\] NOTICE\[716\] chan_sip.c: Call from (.+) to extension '%s' rejected because extension not found in context '%s'." % (regex_date, number, context)
    command = ['less', '/var/log/asterisk/messages', '|', 'grep', '-E', '"%s"' % line_search]
    result = _exec_cmd_to_xivo(command)
    if not result:
        assert(False)


def _exec_cmd_to_xivo(command):
    cmds = []
    for arg in command:
        arg = str(arg)
        arg.encode('utf8')
        cmds.append(arg)

    ssh_command = ['ssh',
                   '-o', 'PreferredAuthentications=publickey',
                   '-o', 'StrictHostKeyChecking=no',
                   '-o', 'UserKnownHostsFile=/dev/null',
                   '-l', 'root',
                   socket.gethostbyname(world.xivo_host)]
    ssh_command.extend(cmds)

    p = Popen(ssh_command,
              stdout=PIPE,
              stderr=STDOUT,
              close_fds=True)
    output = p.communicate()[0]

    if p.returncode != 0:
        print output

    return output
