# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from wazo_test_helpers import until

logger = logging.getLogger(__name__)

WORKER_INSTANCE = 'wazo-auth-worker@1'
WORKER_UNIT_FILE = '/usr/lib/systemd/system/wazo-auth-worker@.service'
REUSE_PORT_CONFIG = '/etc/wazo-auth/conf.d/50-reuse-port.yml'


def is_available(context):
    return context.remote_sysutils.path_exists(WORKER_UNIT_FILE)


def is_active(context):
    output = context.ssh_client.out_call(['systemctl', 'is-active', WORKER_INSTANCE])
    return output.strip() == 'active'


def enable(context):
    sysutils = context.remote_sysutils
    sysutils.write_content_file(REUSE_PORT_CONFIG, 'rest_api:\n  reuse_port: true\n')
    # Restart the primary so it rebinds the port with SO_REUSEPORT before the
    # worker binds the shared port; otherwise the worker fails with EADDRINUSE.
    sysutils.restart_service('wazo-auth')
    context.ssh_client.check_call(['systemctl', 'enable', '--now', WORKER_INSTANCE])
    until.true(
        is_active, context, tries=15, message='HTTP worker did not become active'
    )
    logger.info('wazo-auth HTTP worker %s enabled', WORKER_INSTANCE)


def disable(context):
    context.ssh_client.call(['systemctl', 'disable', '--now', WORKER_INSTANCE])
    context.ssh_client.call(['rm', '-f', REUSE_PORT_CONFIG])
    context.remote_sysutils.restart_service('wazo-auth')
