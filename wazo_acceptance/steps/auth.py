# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
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


@given('I create a mobile session with username "{username}" password "{password}"')
def given_i_create_a_mobile_session(context, username, password):
    _create_token(context, username, password, session_type='mobile')


@when('"{username}" changes its password from "{old_password}" to "{new_password}"')
def step_impl(context, username, old_password, new_password):
    auth = AuthClient(
        username=username,
        password=old_password,
        **context.wazo_config['auth']
    )
    result = auth.token.new()
    auth.set_token(result['token'])

    auth.users.change_password(
        result['metadata']['uuid'],
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
