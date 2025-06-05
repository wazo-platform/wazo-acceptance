# Copyright 2015-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import docker
from playwright.sync_api import Browser, Page
from wazo_test_helpers import until

from wazo_acceptance.helpers.phone import Phone

CONTAINER_NAME = 'acceptance-webrtc-test-helper'
EXPOSED_PORT = 3000


class WebRTCPhone(Phone):

    def __init__(self, context, browser: Browser, page: Page, sipUsername: str, sipPassword: str):
        self.page = page
        self._browser = browser
        self._client = docker.from_env()

        containers = self._client.containers.list(all=True, filters={'name': CONTAINER_NAME})
        for container in containers:
            if container.status == 'running':
                container.kill()
                # kill is enough, container is started with auto-remove, see below

        until.true(
            function=lambda: len(self._client.containers.list(all=True, filters={'name': CONTAINER_NAME})) == 0,
            message="Timeout when waiting for webrtc docker container to stop/remove",
            timeout=10,
            tries=3,
            interval=1
        )

        self._phoneContainer = self._client.containers.run(
            'wazoplatform/wazo-webrtc-test-helper',
            auto_remove=True,
            detach=True,
            name=CONTAINER_NAME,
            ports={'3000/tcp': ('127.0.0.1', EXPOSED_PORT)}
        )

        def openPage(dst):
            try:
                self.page.goto(dst)
                return True
            except Exception:
                return False

        until.true(
            openPage, f"https://{context.wazo_config['wazo_host']}/api/auth/0.1/tokens",
            message="Timeout when waiting to open Wazo page to accept self signed certificate",
            timeout=10,
            tries=3,
            interval=1
        )

        until.true(
            openPage, f'http://localhost:{EXPOSED_PORT}',
            message="Timeout when waiting for WebRTC docker container to start",
            timeout=15,
            tries=5,
            interval=2
        )

        self.page.wait_for_selector('#sipServerHost')
        self.page.locator('#sipServerHost').fill(context.wazo_config['wazo_host'])
        self.page.locator('#sipDomain').fill(context.wazo_config['wazo_host'])
        self.page.locator('#sipUser').fill(sipUsername)
        self.page.locator('#sipPassword').fill(sipPassword)

        context.add_cleanup(self.terminate)

    def call(self, exten):
        self.page.locator('#callDestination').fill(exten)
        self.page.get_by_role("button", name="Call").click()

    def get_codecs(self):
        incomingLocator = self.page.locator('#incoming')
        outgoingLocator = self.page.locator('#outgoing')
        incomingLocator.wait_for(state='visible')
        outgoingLocator.wait_for(state='visible')
        incoming = incomingLocator.text_content().replace('audio/', '')
        outgoing = outgoingLocator.text_content().replace('audio/', '')
        return (incoming, outgoing)

    def hangup(self):
        self.page.get_by_role("button", name="Hangup").click()

    def terminate(self):
        if self._browser:
            self._browser.close()
            self._browser = None
        if self._phoneContainer:
            self._phoneContainer.stop()
            self._phoneContainer = None
