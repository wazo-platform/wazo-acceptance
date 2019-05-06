# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, is_not, none
from behave import then

from xivo_auth_client import Client as AuthClient


@then('I can create an admin token')
def then_i_can_create_a_token(context):
    auth = AuthClient(
        username='root',
        password='wazosecret',
        **context.wazo_config['auth']
    )
    token = auth.token.new()
    assert_that(token['token'], is_not(none()))
