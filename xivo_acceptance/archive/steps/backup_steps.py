# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from lettuce import step, world
from xivo_acceptance.lettuce import assets, auth

logger = logging.getLogger(__name__)


@step(u'Given the asset file "([^"]*)" is copied on the server into "([^"]*)"')
def given_the_file_is_copied_on_the_server_into_group2(step, assetfile, serverpath):
    assets.copy_asset_to_server(assetfile, serverpath)


@step(u'When I execute database backup command')
def when_i_execute_database_backup_command(step):
    command = 'bash /tmp/xivo-backup-manager backup db'
    world.ssh_client_xivo.call([command])


@step(u'Then executing "([^"]*)" should complete without errors')
def when_i_execute_without_error(step, command):
    world.ssh_client_xivo.call([command])


@step(u'When I execute database restore command')
def when_i_execute_database_restore_command(step):
    command = 'bash /tmp/xivo-backup-manager restore db'
    world.ssh_client_xivo.call([command])
    auth.renew_auth_token()
