# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import threading
from contextlib import contextmanager

task_uuid = None


class Bus:

    def __init__(self, websocketd_client):
        self._websocketd_client = websocketd_client

    @contextmanager
    def wait_for_dialplan_reload(self):
        with self._wait_for_asterisk_reload('dialplan reload'):
            yield

    @contextmanager
    def wait_for_pjsip_reload(self):
        with self._wait_for_asterisk_reload('pjsip reload'):
            yield

    @contextmanager
    def _wait_for_asterisk_reload(self, reload_command):
        # WARNING: context manager cannot be nested
        def asterisk_reload(data):
            if data['command'] != reload_command:
                return

            global task_uuid
            if data['status'] == 'starting':
                task_uuid = data['uuid']
            elif data['status'] == 'completed' and task_uuid == data['uuid']:
                # TODO expose close method on wazo-websocketd-client
                self._websocketd_client._ws_app.close()

        self._websocketd_client.on('asterisk_reload_progress', asterisk_reload)
        websocket_thread = threading.Thread(target=self._websocketd_client.run)
        websocket_thread.start()
        try:
            yield
        finally:
            timeout = 5
            websocket_thread.join(timeout)
            if websocket_thread.is_alive():
                self._websocketd_client._ws_app.close()
                websocket_thread.join()
            # TODO allow to remove callback on wazo-websocketd-client
            self._websocketd_client._callbacks.pop('asterisk_reload_progress')
            self._websocketd_client._ws_app = None
            self._websocketd_client._is_running = None
