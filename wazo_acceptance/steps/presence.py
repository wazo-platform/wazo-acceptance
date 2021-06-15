# Copyright 2019-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import then
from hamcrest import assert_that, equal_to


@then('"{firstname} {lastname}" has his presence connected')
def then_the_user_has_his_presence_connected(context, firstname, lastname):
    user = context.helpers.user.get_by(firtname=firstname, lastname=lastname)
    presence = context.chatd_client.user_presences.get(user['uuid'])
    assert_that(presence['connected'], equal_to(True))


@then('"{firstname} {lastname}" has his line state to "{line_state}"')
def then_the_user_has_his_line_state_to(context, firstname, lastname, line_state):
    user = context.helpers.user.get_by(firtname=firstname, lastname=lastname)
    presence = context.chatd_client.user_presences.get(user['uuid'])
    assert_that(presence['line_state'], equal_to(line_state))
