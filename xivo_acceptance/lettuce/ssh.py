# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
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

import logging
import os
import subprocess
from subprocess import PIPE, STDOUT

SSH_OPTIONS = [
    '-o', 'PreferredAuthentications=publickey',
    '-o', 'StrictHostKeyChecking=no',
    '-o', 'UserKnownHostsFile=/dev/null',
]
logger = logging.getLogger(__name__)


class SSHClient(object):

    _fobj_devnull = open(os.devnull, 'r+')

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
        command_result = self._exec_ssh_command(remote_command)
        return command_result.returncode

    def check_call(self, remote_command):
        command_result = self._exec_ssh_command(remote_command, err_in_out=True)
        if command_result.returncode != 0:
            logger.error(command_result.stdout_result)
            raise Exception('Remote command %r returned non-zero exit status %r' %
                            (remote_command, command_result.returncode))
        return command_result.returncode

    def out_call(self, remote_command):
        command_result = self._exec_ssh_command(remote_command)
        if command_result.returncode != 0:
            print command_result.stderr_result
        return command_result.stdout_result

    def out_err_call(self, remote_command):
        command_result = self._exec_ssh_command(remote_command, err_in_out=True)
        return command_result.stdout_result

    def new_process(self, remote_command, *args, **kwargs):
        kwargs.setdefault('close_fds', True)
        command = self._format_ssh_command(remote_command)

        return subprocess.Popen(command, *args, **kwargs)

    def _exec_ssh_command(self, remote_command, err_in_out=False):
        command = self._format_ssh_command(remote_command)
        stderr = STDOUT if err_in_out else PIPE
        p = subprocess.Popen(command,
                             stdin=PIPE,
                             stdout=PIPE,
                             stderr=stderr,
                             close_fds=True)
        (p.stdout_result, p.stderr_result) = p.communicate()
        return p

    def _format_ssh_command(self, remote_command):
        ssh_command = ['ssh']
        ssh_command.extend(SSH_OPTIONS)
        ssh_command.extend(['-l', self._login, self._hostname])
        ssh_command.extend([s.encode('utf-8') for s in remote_command])
        return ssh_command
