# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given, when
from .. import auth

BACKUP_MANAGER = 'wazo-backup-manager'
SERVER_PATH = '/tmp'


@given('the backup manager asset is copied on the server')
def given_the_backup_manager_asset_is_copied_on_the_server(context):
    context.helpers.asset.copy_asset_to_server(BACKUP_MANAGER, SERVER_PATH)


@when('I execute database backup command')
def when_i_execute_database_backup_command(context):
    command = 'bash {server_path}/{backup_manager} backup db'.format(
        server_path=SERVER_PATH,
        backup_manager=BACKUP_MANAGER,
    )
    context.ssh_client.check_call([command])


@when('I execute database restore command')
def when_i_execute_database_restore_command(context):
    command = 'bash {server_path}/{backup_manager} restore db'.format(
        server_path=SERVER_PATH,
        backup_manager=BACKUP_MANAGER,
    )
    context.ssh_client.check_call([command])
    auth.renew_auth_token(context)
