# Copyright 2019-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import then
from hamcrest import assert_that, equal_to

from xivo_test_helpers import until


@then('"{firstname} {lastname}" has "{nb_session}" session in his presence')
def then_the_user_has_number_session_from_his_presence(context, firstname, lastname, nb_session):
    user = context.helpers.user.get_by(firtname=firstname, lastname=lastname)
    presence = context.chatd_client.user_presences.get(user['uuid'])
    assert_that(len(presence['sessions']), equal_to(int(nb_session)))


@then('"{firstname} {lastname}" has his line state to "{line_state}"')
def then_the_user_has_his_line_state_to(context, firstname, lastname, line_state):
    user = context.helpers.user.get_by(firtname=firstname, lastname=lastname)

    def check_line_state():
        presence = context.chatd_client.user_presences.get(user['uuid'])
        assert_that(presence['line_state'], equal_to(line_state))

    # NOTE(fblackburn): When this step is executed after the event received step, then a race
    # condition can occurs (mostly on single core host) between the event sent and the database
    # commit
    until.assert_(check_line_state, interval=0.2, tries=2)
