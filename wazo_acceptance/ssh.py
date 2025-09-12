# Copyright 2013-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import os
import random
import string
import subprocess
from subprocess import PIPE, STDOUT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    class PatchedPopen(subprocess.Popen):
        stdout_result: str
        stderr_result: str


SSH_OPTIONS = [
    '-o', 'PreferredAuthentications=publickey',
    '-o', 'StrictHostKeyChecking=no',
    '-o', 'UserKnownHostsFile=/dev/null',
]
logger = logging.getLogger(__name__)


class SSHClient:

    _fobj_devnull = open(os.devnull, 'r+')

    def __init__(self, host, login, sudo, sudo_shell):
        self._hostname = host
        self._login = login
        self._sudo = sudo
        self._sudo_shell = sudo_shell

    def send_files(self, path_from, path_to):
        wazo_ssh = f'{self._login}@{self._hostname}'
        scp_dest = path_to
        if self._sudo:
            random_str = "".join(
                random.choice(string.ascii_letters + string.digits) for _ in range(12)
            )
            scp_dest = f'/tmp/{random_str}'
        cmd = [f'{path_from}', f'{wazo_ssh}:{scp_dest}']
        scp_command = [
            'scp',
            '-o', 'PreferredAuthentications=publickey',
            '-o', 'StrictHostKeyChecking=no',
            '-o', 'UserKnownHostsFile=/dev/null',
        ]
        scp_command.extend(cmd)

        logger.debug(f'Copying {path_from} to {scp_dest}')
        scp_result = subprocess.call(
            scp_command,
            stdout=PIPE,
            stderr=STDOUT,
            close_fds=True,
        )
        logger.debug(scp_result)
        if self._sudo:
            dest_full_path = os.path.join(path_to, os.path.basename(path_from))
            logger.debug(f'Sudo mode. Moving {scp_dest} to {dest_full_path}')
            cmd_result = self._exec_ssh_command(["mv", scp_dest, dest_full_path], err_in_out=True)
            logger.debug(cmd_result)
            logger.debug(f'Sudo mode. Setting ownership of {dest_full_path}')
            cmd_result = self._exec_ssh_command(["chown", "root:root", dest_full_path], err_in_out=True)
            logger.debug(cmd_result)
        return scp_result

    def call(self, remote_command):
        command_result = self._exec_ssh_command(remote_command)
        return command_result.returncode

    def check_call(self, remote_command):
        command_result = self._exec_ssh_command(remote_command, err_in_out=True)
        if command_result.returncode != 0:
            logger.error(command_result.stdout_result)
            raise Exception(
                'Remote command {cmd} returned non-zero exit status {code}'.format(
                    cmd=remote_command,
                    code=command_result.returncode
                )
            )
        return command_result.returncode

    def out_call(self, remote_command):
        command_result = self._exec_ssh_command(remote_command)
        if command_result.returncode != 0:
            print(command_result.stderr_result)
        return command_result.stdout_result

    def out_err_call(self, remote_command):
        command_result = self._exec_ssh_command(remote_command, err_in_out=True)
        return command_result.stdout_result

    def new_process(self, remote_command, *args, force_tty=False, **kwargs):
        kwargs.setdefault('close_fds', True)
        ssh_options = []
        if force_tty:
            ssh_options = ['-o', 'RequestTTY=force']
        if self._sudo:
            remote_command = ["sudo"] + remote_command
        command = self._format_ssh_command(remote_command, *ssh_options)

        process = subprocess.Popen(command, *args, **kwargs)
        return process

    def _exec_ssh_command(self, remote_command: [str], err_in_out: bool = False) -> PatchedPopen:
        if self._sudo:
            remote_command = ["sudo", self._sudo_shell, "-c", '"' + " ".join([c.replace('"', '\\"').replace('$', '\\$') for c in remote_command]) + '"']
            logger.debug(" ".join(remote_command))
        command = self._format_ssh_command(remote_command)
        stderr = STDOUT if err_in_out else PIPE
        p = subprocess.Popen(
            command,
            stdin=PIPE,
            stdout=PIPE,
            stderr=stderr,
            close_fds=True,
            text=True,
        )
        p.stdout_result, p.stderr_result = p.communicate()
        return p

    def _format_ssh_command(self, remote_command, *extended_options):
        ssh_command = ['ssh']
        ssh_command.extend(SSH_OPTIONS)
        ssh_command.extend(extended_options)
        ssh_command.extend(['-l', self._login, self._hostname])
        ssh_command.extend([s.encode('utf-8') for s in remote_command])
        return ssh_command
