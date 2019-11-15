# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given, then


@given('the asset file "{filename}" is copied on the server into "{directory}"')
def given_the_asset_file_is_copied_on_the_server(context, filename, directory):
    context.helpers.asset.copy_asset_to_server(filename, directory)


@then('executing "{file_}" should complete without errors')
def then_executing_file_should_complete_without_errors(context, file_):
    context.ssh_client.check_call([file_])
