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
from subprocess import PIPE, STDOUT


class SSHClient(object):
    def __init__(self, hostname, login):
        self._hostname = hostname
        self._login = login

    def send_files(self, path_from, path_to):
        xivo_ssh = '%s@%s' % (self._login, self._hostname)
        cmd = ['%s' % path_from, '%s:%s' % (xivo_ssh, path_to)]
        scp_command = ['scp',
                       '-o', 'PreferredAuthentications=publickey',
                       '-o', 'StrictHostKeyChecking=no',
                       '-o', 'UserKnownHostsFile=/dev/null']
        scp_command.extend(cmd)

        return subprocess.call(scp_command,
                               stdout=PIPE,
                               stderr=STDOUT,
                               close_fds=True)

    def call(self, remote_command):
        return self._exec_ssh_command(remote_command)

    def check_call(self, remote_command):
        retcode = self._exec_ssh_command(remote_command)
        if retcode != 0:
            raise Exception('Remote command %r returned non-zero exit status %r' %
                            (remote_command, retcode))
        return retcode

    def out_call(self, remote_command):
        return self._exec_ssh_command_with_return_stdout(remote_command)

    def out_err_call(self, remote_command):
        return self._exec_ssh_command_with_return_stdout_stderr(remote_command)

    def new_process(self, remote_command, *args, **kwargs):
        kwargs.setdefault('close_fds', True)
        command = self._format_ssh_command(remote_command)

        return subprocess.Popen(command, *args, **kwargs)

    def _exec_ssh_command(self, remote_command):
        command = self._format_ssh_command(remote_command)

        return subprocess.call(command,
                               stdout=PIPE,
                               stderr=STDOUT,
                               close_fds=True)

    def _exec_ssh_command_with_return_stdout(self, remote_command):
        command = self._format_ssh_command(remote_command)

        p = subprocess.Popen(command,
                             stdin=PIPE,
                             stdout=PIPE,
                             stderr=PIPE,
                             close_fds=True)

        (stdoutdata, stderrdata) = p.communicate()

        if p.returncode != 0:
            print stderrdata

        return stdoutdata

    def _exec_ssh_command_with_return_stdout_stderr(self, remote_command):
        command = self._format_ssh_command(remote_command)

        p = subprocess.Popen(command,
                             stdin=PIPE,
                             stdout=PIPE,
                             stderr=STDOUT,
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
