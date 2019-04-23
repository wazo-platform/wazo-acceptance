# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import (
    assert_that,
    equal_to,
    is_,
)
from lettuce import step
from xivo_acceptance.helpers import (
    user_helper,
    user_line_extension_helper as ule_helper,
)


@step(u'^Given there are users with infos:$')
def given_there_are_users_with_infos(step):
    """step: Given there are users with infos:

    :param step: hashes
    :type step: list

    .. note::
        note

    :Example:

    Scenario: Create Users
        Given there are users with infos:
        | firstname | lastname | number | context | ... |

    Columns are:
        entity_name
        firstname
        lastname
        number
        context
        cti_profile
        cti_login
        cti_passwd
        agent_number
        language
        voicemail_name
        voicemail_number
        mobile_number
        group_name
        group_chantype
        protocol
        device
        with_phone (yes/no)
        max_contacts
        token (yes/no)
    """
    for user_data in step.hashes:
        user_helper.add_user_with_infos(user_data, step=step)


@step(u'Given there is no user "([^"]*)" "([^"]*)"$')
def given_there_is_a_no_user_1_2(step, firstname, lastname):
    ule_helper.delete_user_line_extension_voicemail(firstname, lastname)


@step(u'Given user "([^"]*)" "([^"]*)" has the following function keys:')
def given_user_has_the_following_function_keys(step, firstname, lastname):
    pass


@step(u'Given "([^"]*)" has a dialaction on "([^"]*)" to "([^"]*)" "([^"]*)"')
def given_user_has_a_dialaction(step, fullname, event, dialaction, destination):
    pass


@step(u'Given "([^"]*)" has a "([^"]*)" seconds ringing time')
def given_user_has_a_n_ringing_time(step, fullname, ring_seconds):
    pass


@step(u'Given user "([^"]*)" "([^"]*)" has schedule "([^"]*)"')
def given_user_1_has_schedule_2(step, firstname, lastname, schedule):
    user = user_helper.get_by_firstname_lastname(firstname, lastname)
    user_helper.associate_schedule(schedule, user['id'])


@step(u'When I reorder "([^"]*)" "([^"]*)"s function keys such that:')
def when_i_reorder_group1_group2_s_function_keys_such_that(step, firstname, lastname):
    pass


@step(u'Then the user "([^"]*)" "([^"]*)" not exist')
def then_the_user_not_exist(step, firstname, lastname):
    pass


@step(u'Then I see a user with infos:')
def then_i_see_a_user_with_infos(step):
    pass


@step(u'Then "([^"]*)" has an unconditional forward set to "([^"]*)"')
def then_user_has_an_unconditional_forward_set_to_group2(step, fullname, expected_destination):
    enabled, destination = user_helper.get_unconditional_forward(fullname)
    assert_that(enabled)
    assert_that(destination, equal_to(expected_destination))


@step(u'Then "([^"]*)" has no unconditional forward')
def then_user_has_no_unconditional_forward(step, fullname):
    enabled, _ = user_helper.get_unconditional_forward(fullname)
    assert_that(enabled, is_(False))
