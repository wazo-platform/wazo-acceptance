# Copyright 2019-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, is_not, none
from behave import (
    given,
    then,
    when,
)

from wazo_auth_client import Client as AuthClient


@then('I can create an admin token')
def then_i_can_create_a_token(context):
    token = _create_token(context, 'root', 'wazosecret')
    assert_that(token['token'], is_not(none()))


@then('I can get a user token with username "{username}" and password "{password}"')
def then_i_can_get_a_user_token(context, username, password):
    token = _create_token(context, username, password)
    assert_that(token['token'], is_not(none()))


@when('I create a session with username "{username}" password "{password}"')
def when_i_create_a_session(context, username, password):
    _create_token(context, username, password)


@given('I create a mobile session with username "{username}" password "{password}"')
def given_i_create_a_mobile_session(context, username, password):
    _create_token(context, username, password, session_type='mobile')


@when('"{username}" changes its password from "{old_password}" to "{new_password}"')
def user_changes_its_password_from_old_to_new(context, username, old_password, new_password):
    token = _create_token(context, username, old_password)
    with context.helpers.utils.set_token(context.auth_client, token['token']):
        context.auth_client.users.change_password(
            token['metadata']['uuid'],
            old_password=old_password,
            new_password=new_password,
        )


def _create_token(context, username, password, **kwargs):
    auth = AuthClient(
        username=username,
        password=password,
        **context.wazo_config['auth']
    )
    return auth.token.new(**kwargs)
