# Copyright 2019-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import functools
import logging
import queue
import threading
from contextlib import contextmanager

from hamcrest import assert_that, has_entries
from wazo_test_helpers import until

logger = logging.getLogger(__name__)
tasks: dict[str, str | None] = None  # type: ignore[assignment]


class Bus:

    def __init__(self, context):
        self._context = context
        self._websocketd_client = context.websocketd_client
        self._websocket_ready = False
        self._websocket_thread = None
        self._received_events = None

    @contextmanager
    def wait_for_asterisk_reload(self, dialplan=False, pjsip=False, queue=False,
                                 confbridge=False, voicemail=False, parking=False):
        commands = []
        if dialplan:
            commands.append('dialplan reload')
        if pjsip:
            commands.append('module reload res_pjsip.so')
        if queue:
            commands.append('module reload app_queue.so')
        if confbridge:
            commands.append('module reload app_confbridge.so')
        if voicemail:
            commands.append('voicemail reload')
        if parking:
            commands.append('module reload res_parking.so')

        if not commands:
            raise Exception('No wait module specified')

        with self._wait_for_asterisk_reload(commands):
            yield

    @contextmanager
    def _wait_for_asterisk_reload(self, reload_commands):
        global tasks
        tasks = {command: None for command in reload_commands}

        def asterisk_reload(event):
            if not self._websocket_ready:
                # event was triggered by a previous action
                return

            global tasks
            data = event['data']
            command = data['command']
            if command not in tasks:
                return

            task_uuid = data['uuid']
            if data['status'] == 'starting':
                tasks[command] = task_uuid
            elif data['status'] == 'completed' and task_uuid in tasks.values():
                tasks.pop(command)
                if not tasks:
                    self._websocketd_client.stop()

        self._websocketd_client.on('asterisk_reload_progress', asterisk_reload)
        with self._managed_bus_connection(reload_commands):
            yield

    @contextmanager
    def wait_for_event(self, event_name, expected_data):
        def event_received(data):
            if not self._websocket_ready:
                # event was triggered by a previous action
                return

            try:
                assert_that(data['data'], has_entries(**expected_data))
            except AssertionError:
                return
            self._websocketd_client.stop()

        self._websocketd_client.on(event_name, event_received)
        with self._managed_bus_connection(event_name):
            yield

    @contextmanager
    def _managed_bus_connection(self, event_name):
        self._start()
        try:
            yield
        finally:
            self._websocket_thread.join(timeout=self._context.wazo_config['reload_timeout'])
            if self._websocket_thread.is_alive():
                logger.warning('No event received for %s', event_name)
            self._stop()

    def subscribe(self, events):
        if self._websocket_thread:
            self._stop()

        for event in events:
            self._websocketd_client.on(
                event,
                functools.partial(self._save_event, event)
            )
        self._start()
        self._context.add_cleanup(self._stop)

    def _save_event(self, name, event):
        self._received_events.put(event)

    def pop_received_event(self, timeout=None):
        timeout = timeout or self._context.wazo_config['reload_timeout']
        if self._websocket_thread is None:
            raise RuntimeError("websocket thread not started")
        return self._received_events.get(timeout=timeout)

    def _start(self):
        if self._websocket_thread:
            logger.error("websocket thread already started. Stopping.")
            self._stop()
        self._received_events = queue.Queue()
        self._websocket_thread = threading.Thread(target=self._websocketd_client.run)
        logger.debug('Starting websocketd client thread...')
        self._websocket_thread.start()

        logger.debug('Waiting for websocket to be ready...')
        try:
            until.true(lambda: self._websocketd_client.is_running, interval=0.5, timeout=5)
        except until.NoMoreTries:
            self._websocketd_client.stop()
            self._websocket_thread.join()
            raise
        self._websocket_ready = True
        logger.debug('Websocket ready')

    def _stop(self):
        if self._websocket_thread.is_alive():
            self._websocketd_client.stop()
            self._websocket_thread.join()
        self._received_events = None
        self._websocket_thread = None
        self._websocket_ready = False
