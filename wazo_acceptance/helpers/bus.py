# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import threading
from contextlib import contextmanager

tasks = None


class Bus:

    def __init__(self, websocketd_client):
        self._websocketd_client = websocketd_client

    @contextmanager
    def wait_for_asterisk_reload(self, dialplan=False, pjsip=False, queue=False):
        commands = []
        if dialplan:
            commands.append('dialplan reload')
        if pjsip:
            commands.append('module reload res_pjsip.so')
        if queue:
            commands.append('module reload app_queue.so')

        if not commands:
            raise Exception('No wait module specified')

        with self._wait_for_asterisk_reload(commands):
            yield

    @contextmanager
    def wait_for_dialplan_reload(self):
        with self._wait_for_asterisk_reload(['dialplan reload']):
            yield

    @contextmanager
    def wait_for_pjsip_reload(self):
        with self._wait_for_asterisk_reload(['module reload res_pjsip.so']):
            yield

    @contextmanager
    def _wait_for_asterisk_reload(self, reload_commands):
        global tasks
        tasks = {command: None for command in reload_commands}

        def asterisk_reload(data):
            global tasks
            command = data['command']
            if command not in tasks:
                return

            task_uuid = data['uuid']
            if data['status'] == 'starting':
                tasks[command] = task_uuid
            elif data['status'] == 'completed' and task_uuid in tasks.values():
                tasks.pop(command)
                if not tasks:
                    # TODO expose close method on wazo-websocketd-client
                    self._websocketd_client._ws_app.close()

        self._websocketd_client.on('asterisk_reload_progress', asterisk_reload)
        websocket_thread = threading.Thread(target=self._websocketd_client.run)
        websocket_thread.start()
        try:
            yield
        finally:
            websocket_thread.join(timeout=5)
            if websocket_thread.is_alive():
                self._websocketd_client._ws_app.close()
                websocket_thread.join()
            # TODO allow to remove callback on wazo-websocketd-client
            self._websocketd_client._callbacks.pop('asterisk_reload_progress')
            self._websocketd_client._ws_app = None
            self._websocketd_client._is_running = None
