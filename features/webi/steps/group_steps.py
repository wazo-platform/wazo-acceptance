# -*- coding: utf-8 -*-

from lettuce import step
from xivo_lettuce import form
from xivo_lettuce.common import open_url, element_in_list_matches_field
from xivo_lettuce.manager.group_manager import remove_group_with_name, \
    type_group_name, type_group_number, type_context
from xivo_lettuce.manager_ws import group_manager_ws
from xivo_lettuce.manager_ws.user_manager_ws import find_user_id_with_firstname_lastname
from xivo_lettuce.manager_ws import user_manager_ws
from utils.func import extract_number_and_context_from_extension


@step(u'Given there is a group "([^"]*)" with extension "([^"]*)" and users:')
def given_there_is_a_group_with_extension_and_users(step, name, extension):
    number, context = extract_number_and_context_from_extension(extension)
    group_manager_ws.delete_groups_with_number(number)

    user_ids = []
    for info in step.hashes:
        user_id = find_user_id_with_firstname_lastname(info['firstname'], info['lastname'])
        user_ids.append(user_id)

    group_manager_ws.add_group(name, number, context, user_ids)


@step(u'Given there is no group with name "([^"]*)"')
def given_there_is_no_group_with_name(step, name):
    group_manager_ws.delete_groups_with_name(name)


@step(u'When I create a group "([^"]*)" with number "([^"]*)"')
def when_i_create_group_with_number(step, group_name, group_number):
    open_url('group', 'add')
    type_group_name(group_name)
    type_group_number(group_number)
    type_context('default')
    form.submit.submit_form()


@step(u'When I set a group "([^"]*)" with number "([^"]*)"')
def when_i_set_a_group_with_number_(step, group_name, group_number):
    open_url('group', 'add')
    type_group_name(group_name)
    type_group_number(group_number)
    type_context('default')


@step(u'When group "([^"]*)" is removed')
def when_group_is_removed(step, group_name):
    remove_group_with_name(group_name)


@step(u'Then I see a group "([^"]*)" with no users')
def then_I_see_a_group_1_with_no_users(step, group_name):
    element_in_list_matches_field('group', group_name, 'nbqmember', 0)


@step(u'Given there is a group with "(\d+)" users')
def given_there_is_a_group_with_n_users(step, group_size):
    group_name = 'random'
    group_members = []
    for i in range(int(group_size)):
        user_id = user_manager_ws.add_or_replace_user(
            {'firstname': 'random',
             'lastname': str(i),
             'line_number': str(1100 + i),
             'line_context': 'default'})
        group_members.append(user_id)

    group_manager_ws.add_or_replace_group(group_name, user_ids=group_members)
