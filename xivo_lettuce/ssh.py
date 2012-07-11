# -*- coding: UTF-8 -*-

import subprocess
from subprocess import PIPE


class SSHClient(object):
    def __init__(self, hostname, login):
        self._hostname = hostname
        self._login = login

    def call(self, remote_command):
        return self._exec_ssh_command(remote_command)

    def _exec_ssh_command(self, remote_command):
        command = self._format_ssh_command(remote_command)
        return subprocess.call(command)

    def _exec_ssh_command_with_return(self, remote_command):
        command = self._format_ssh_command(remote_command)
        p = subprocess.Popen(command,
                             stdout=PIPE,
                             stderr=PIPE,
                             close_fds=True)

        (stdoutdata, stderrdata) = p.communicate()

        return stdoutdata

    def _format_ssh_command(self, remote_command):
        ssh_command = ['ssh',
                       '-o', 'PreferredAuthentications=publickey',
                       '-o', 'StrictHostKeyChecking=no',
                       '-o', 'UserKnownHostsFile=/dev/null',
                       '-l', self._login,
                       self._hostname]
        ssh_command.extend(remote_command)
        return ssh_command

    def check_call(self, remote_command):
        retcode = self._exec_ssh_command(remote_command)
        if retcode != 0:
            raise Exception('Remote command %r returned non-zero exit status %r' %
                            (remote_command, retcode))
        return retcode

    def out_call(self, remote_command):
        return self._exec_ssh_command_with_return(remote_command)
