# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step
from lettuce import world

from xivo_acceptance.helpers import user_helper, group_helper
from xivo_acceptance.helpers import user_line_extension_helper as ule_helper
from xivo_acceptance.lettuce import func


@step(u'Given there is no group "([^"]*)"$')
def given_there_is_no_group(step, search):
    pass


@step(u'Given there are groups:')
def given_there_are_groups(step):
    pass


@step(u'Given there is a group "([^"]*)" with extension "([^"]*)" and users:$')
def given_there_is_a_group_with_extension_and_users(step, name, extension):
    number, context = func.extract_number_and_context_from_extension(extension)

    users = []
    for info in step.hashes:
        user = user_helper.get_by_firstname_lastname(info['firstname'], info.get('lastname'))
        users.append(user)

    group_helper.add_or_replace_group(name, number, context, users)


@step(u'Given the group named "([^"]*)" does not exist')
def given_the_group_named_1_does_not_exist(step, name):
    group_helper.delete_groups_with_name(name)


@step(u'Given there is a group with "(\d+)" users')
def given_there_is_a_group_with_n_users(step, group_size):
    group_name = 'random'
    group_members = []
    for i in range(int(group_size)):
        user_id = ule_helper.add_or_replace_user(
            {'firstname': 'random',
             'lastname': str(i),
             'line_number': str(1100 + i),
             'line_context': 'default'}, step=step)
        user = world.confd_client.users.get(user_id)
        group_members.append(user)

    group_helper.add_or_replace_group(group_name, users=group_members)


@step(u'When I create a group "([^"]*)" with number "([^"]*)"$')
def when_i_create_group_with_number(step, group_name, group_number):
    pass


@step(u'When I create a group "([^"]*)" with number "([^"]*)" with errors')
def when_i_create_group_with_number_with_errors(step, group_name, group_number):
    pass


@step(u'When I remove the group "([^"]*)"')
def when_i_remove_the_group_1(step, group_name):
    pass


@step(u'Then I see a group "([^"]*)" with no users')
def then_I_see_a_group_1_with_no_users(step, group_name):
    pass


@step(u'Then I see the group "([^"]*)" exists$')
def then_i_see_the_element_exists(step, name):
    pass


@step(u'Then I see the group "([^"]*)" not exists$')
def then_i_see_the_element_not_exists(step, name):
    pass
