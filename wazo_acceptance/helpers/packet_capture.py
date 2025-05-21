# Copyright 2023-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import signal
from datetime import datetime
from subprocess import Popen, TimeoutExpired

from ..ssh import SSHClient

TCPDUMP_OUTPUT_DIR = '/tmp/commands/tcpdump'
SNGREP_OUTPUT_DIR = '/tmp/commands/sngrep'


class _PacketCapture:
    def __init__(self, ssh_client: SSHClient) -> None:
        self._ssh_client = ssh_client
        self._current_process: Popen | None = None
        self.setup()

    @property
    def is_running(self) -> bool:
        return self._current_process is not None and self._current_process.poll() is None

    def setup(self) -> None:
        self._ssh_client.check_call(['mkdir', '-p', self.output_dir])

    def start(self, log_name: str) -> None:
        raise NotImplementedError()

    def stop(self) -> None:
        if self.is_running:
            self._current_process.send_signal(signal.SIGINT)
            try:
                self._current_process.wait(timeout=1)
            except TimeoutExpired:
                self._current_process.send_signal(signal.SIGTERM)
                self._current_process.wait(timeout=10)
            self._current_process = None


class TCPDump(_PacketCapture):
    output_dir = TCPDUMP_OUTPUT_DIR

    def start(self, log_name: str) -> None:
        if self.is_running:
            raise RuntimeError('Already running')

        timestamp = datetime.now().timestamp()
        name = log_name.replace(' ', '_').lower()
        command = [
            '/usr/bin/tcpdump',
            '-w',
            f'{self.output_dir}/{timestamp}_{name}.pcap',
            'port',
            'not',
            '22',
        ]
        self._current_process = self._ssh_client.new_process(command, force_tty=True)


class SNGrep(_PacketCapture):
    output_dir = SNGREP_OUTPUT_DIR

    def start(self, log_name: str) -> None:
        if self.is_running:
            raise RuntimeError('Already running')

        timestamp = datetime.now().timestamp()
        name = log_name.replace(' ', '_').lower()
        command = [
            '/usr/bin/sngrep',
            '--no-interface',
            '--quiet',
            '--output',
            f'{self.output_dir}/{timestamp}_{name}.pcap',
        ]
        self._current_process = self._ssh_client.new_process(command, force_tty=True)
