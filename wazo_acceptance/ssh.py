# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

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
        wazo_ssh = '%s@%s' % (self._login, self._hostname)
        cmd = ['%s' % path_from, '%s:%s' % (wazo_ssh, path_to)]
        scp_command = [
            'scp',
            '-o', 'PreferredAuthentications=publickey',
            '-o', 'StrictHostKeyChecking=no',
            '-o', 'UserKnownHostsFile=/dev/null',
        ]
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
            print(command_result.stderr_result)
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
        p = subprocess.Popen(
            command,
            stdin=PIPE,
            stdout=PIPE,
            stderr=stderr,
            close_fds=True,
        )
        p.stdout_result, p.stderr_result = p.communicate()
        return p

    def _format_ssh_command(self, remote_command):
        ssh_command = ['ssh']
        ssh_command.extend(SSH_OPTIONS)
        ssh_command.extend(['-l', self._login, self._hostname])
        ssh_command.extend([s.encode('utf-8') for s in remote_command])
        return ssh_command
