# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given, when
from .. import assets, auth


@given('the asset file "{assetfile}" is copied on the server into "{serverpath}"')
def given_the_file_is_copied_on_the_server(context, assetfile, serverpath):
    assets.copy_asset_to_server(context, assetfile, serverpath)


@when('I execute database backup command')
def when_i_execute_database_backup_command(context):
    command = 'bash /tmp/xivo-backup-manager backup db'
    context.ssh_client.check_call([command])


@when('I execute database restore command')
def when_i_execute_database_restore_command(context):
    command = 'bash /tmp/xivo-backup-manager restore db'
    context.ssh_client.check_call([command])
    auth.renew_auth_token(context)
