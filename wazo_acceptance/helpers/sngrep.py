# Copyright 2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import signal
from datetime import datetime
from subprocess import Popen

from ..ssh import SSHClient

SNGREP_OUTPUT_DIR = '/tmp/commands/sngrep'


class SNGrep:
    def __init__(self, ssh_client: SSHClient) -> None:
        self._ssh_client = ssh_client
        self._current_process: Popen | None = None
        self.setup()

    @property
    def is_running(self) -> bool:
        return self._current_process is not None and self._current_process.poll() is None

    def setup(self) -> None:
        self._ssh_client.check_call(['mkdir', '-p', SNGREP_OUTPUT_DIR])

    def start(self, log_prefix: str) -> None:
        if self._current_process is not None:
            raise RuntimeError('Already running')

        timestamp = datetime.now().timestamp()
        prefix = log_prefix.replace(' ', '_').lower()
        self._current_process = self._ssh_client.new_process([
            '/usr/bin/sngrep',
            '--no-interface',
            '--quiet',
            '--output',
            f'/{SNGREP_OUTPUT_DIR}/{prefix}_{timestamp}.pcap',
        ])

    def stop(self) -> None:
        if self.is_running:
            self._current_process.send_signal(signal.SIGINT)
            if self.is_running:
                self._current_process.terminate()
                self._current_process.wait()
            self._current_process = None

