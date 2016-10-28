# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from lettuce import step

from xivo_acceptance.action.webi import group as group_action_webi
from xivo_acceptance.helpers import user_helper, group_helper
from xivo_acceptance.helpers import user_line_extension_helper as ule_helper
from xivo_acceptance.lettuce import common, form, func


@step(u'Given there is no group "([^"]*)"$')
def given_there_is_no_group(step, search):
    common.remove_element_if_exist('group', search)


@step(u'Given there are groups:')
def given_there_are_groups(step):
    for group in step.hashes:
        group_helper.delete_groups_with_number(group['exten'])
        group_helper.add_group(
            group['name'],
            group['exten'],
            group['context']
        )
        common.open_url('group', 'list', {'search': group['name']})
        common.edit_line(group['name'])
        if 'ring seconds' in group:
            form.input.set_text_field_with_label('Ring time', '%s' % group['ring seconds'])
        if 'noanswer' in group:
            common.go_to_tab('No answer')
            forward_dest_type, forward_dest_name = group['noanswer'].split(':', 1)
            if forward_dest_type == 'group':
                form.select.set_select_field_with_id('it-dialaction-noanswer-actiontype', 'Group')
                form.select.set_select_field_with_id_containing('it-dialaction-noanswer-group-actionarg1', forward_dest_name)
        form.submit.submit_form()
        common.open_url('group', 'list', {'search': ''})


@step(u'Given there is a group "([^"]*)" with extension "(\d+)@(\w+)"$')
def given_there_is_a_group_with_extension(step, name, number, context):
    group_helper.delete_groups_with_number(number)
    group_helper.add_group(name, number, context)


@step(u'Given there is a group "([^"]*)" with extension "([^"]*)" and users:$')
def given_there_is_a_group_with_extension_and_users(step, name, extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    group_helper.delete_groups_with_number(number)

    user_ids = []
    for info in step.hashes:
        user = user_helper.get_by_firstname_lastname(info['firstname'], info.get('lastname'))
        user_ids.append(user['id'])

    group_helper.add_group(name, number, context, user_ids)


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
        group_members.append(user_id)

    group_helper.add_or_replace_group(group_name, user_ids=group_members)


@step(u'When I create a group "([^"]*)" with number "([^"]*)"$')
def when_i_create_group_with_number(step, group_name, group_number):
    common.open_url('group', 'add')
    _type_group_name_number_context(group_name, group_number)
    form.submit.submit_form()


@step(u'When I create a group "([^"]*)" with number "([^"]*)" with errors')
def when_i_create_group_with_number_with_errors(step, group_name, group_number):
    common.open_url('group', 'add')
    _type_group_name_number_context(group_name, group_number)
    form.submit.submit_form_with_errors()


@step(u'When I remove the group "([^"]*)"')
def when_i_remove_the_group_1(step, group_name):
    group_action_webi.remove_group_with_name(group_name)


@step(u'Then I see a group "([^"]*)" with no users')
def then_I_see_a_group_1_with_no_users(step, group_name):
    common.element_in_list_matches_field('group', group_name, 'nbqmember', 0)


@step(u'Then I see the group "([^"]*)" exists$')
def then_i_see_the_element_exists(step, name):
    common.open_url('group')
    line = common.find_line(name)
    assert line is not None, 'group: %s does not exist' % name


@step(u'Then I see the group "([^"]*)" not exists$')
def then_i_see_the_element_not_exists(step, name):
    common.open_url('group')
    line = common.find_line(name)
    assert line is None, 'group: %s exist' % name


def _type_group_name_number_context(name, number, context='default'):
    group_action_webi.type_group_name(name)
    group_action_webi.type_group_number(number)
    group_action_webi.type_context(context)
