# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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

from hamcrest import assert_that, equal_to
from lettuce import step
from lettuce.registry import world
from selenium.webdriver.support.select import Select

from xivo_acceptance.action.webi import user as user_action_webi
from xivo_acceptance.action.webi import line as line_action_webi
from xivo_acceptance.helpers import user_helper, agent_helper, group_helper, sip_config, sip_phone
from xivo_acceptance.helpers import user_line_extension_helper as ule_helper
from xivo_lettuce import common, form


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
    """
    for user_data in step.hashes:
        _add_user(user_data, step=step)


def _add_user(user_data, step=step):
    user_ws_data = {}
    user_ws_data['firstname'] = user_data['firstname']
    user_ws_data['lastname'] = user_data['lastname']

    if user_data.get('entity_name'):
        user_ws_data['entity_name'] = user_data['entity_name']

    if user_data.get('number') and user_data.get('context'):
        user_ws_data['line_number'] = user_data['number']
        user_ws_data['line_context'] = user_data['context']
        if 'protocol' in user_data:
            user_ws_data['protocol'] = user_data['protocol']
        if 'device' in user_data:
            user_ws_data['device'] = user_data['device']

        if user_data.get('voicemail_name') and user_data.get('voicemail_number'):
            user_ws_data['voicemail_name'] = user_data['voicemail_name']
            user_ws_data['voicemail_number'] = user_data['voicemail_number']

    if user_data.get('bsfilter'):
        user_ws_data['bsfilter'] = user_data['bsfilter']

    if user_data.get('language'):
        user_ws_data['language'] = user_data['language']

    if 'voicemail_name' in user_data and 'language' not in user_data:
        user_ws_data['language'] = 'en_US'

    if user_data.get('cti_profile'):
        user_ws_data['enable_client'] = True
        user_ws_data['client_profile'] = user_data['cti_profile']
        if user_data.get('cti_login'):
            user_ws_data['client_username'] = user_data['cti_login']
        else:
            user_ws_data['client_username'] = user_ws_data['firstname'].lower()
        if user_data.get('cti_passwd'):
            user_ws_data['client_password'] = user_data['cti_passwd']
        else:
            user_ws_data['client_password'] = user_ws_data['lastname'].lower()

    if user_data.get('mobile_number'):
        user_ws_data['mobile_number'] = user_data['mobile_number']

    user_id = ule_helper.add_or_replace_user(user_ws_data, step=step)

    if user_data.get('agent_number'):
        agent_helper.delete_agents_with_number(user_data['agent_number'])
        agent_data = {'firstname': user_data['firstname'],
                      'lastname': user_data['lastname'],
                      'number': user_data['agent_number'],
                      'context': user_data.get('context', 'default'),
                      'users': [int(user_id)]}
        agent_helper.add_agent(agent_data)

    if user_data.get('group_name'):
        group_helper.add_or_replace_group(user_data['group_name'], user_ids=[user_id])


@step(u'Given there is no user "([^"]*)" "([^"]*)"$')
def given_there_is_a_no_user_1_2(step, firstname, lastname):
    ule_helper.delete_user_line_extension_with_firstname_lastname(firstname, lastname)


@step(u'Given user "([^"]*)" "([^"]*)" has the following function keys:')
def given_user_has_the_following_function_keys(step, firstname, lastname):
    common.open_url('user', 'search', {'search': '%s %s' % (firstname, lastname)})
    common.edit_line("%s %s" % (firstname, lastname))
    name_map = {
        'Key': 'key_number',
        'Type': 'key_type',
        'Destination': 'destination',
        'Label': 'label',
        'Supervision': 'supervised',
    }
    for key_definition in step.hashes:
        key = dict((name_map[k], v) for k, v in key_definition.iteritems())
        user_action_webi.type_func_key(**key)
    form.submit.submit_form()


@step(u'When I reorder "([^"]*)" "([^"]*)"s function keys such that:')
def when_i_reorder_group1_group2_s_function_keys_such_that(step, firstname, lastname):
    common.open_url('user', 'search', {'search': '%s %s' % (firstname, lastname)})
    common.edit_line("%s %s" % (firstname, lastname))
    pairs = [(k['Old'], k['New']) for k in step.hashes]
    user_action_webi.change_key_order(pairs)
    form.submit.submit_form()


@step(u'When I create a user with infos:$')
def when_i_create_a_user(step):
    common.open_url('user', 'add')
    user_properties = step.hashes[0]
    user_action_webi.type_user_names(user_properties['firstname'], user_properties.get('lastname', ''))
    if 'number' in user_properties:
        user_action_webi.user_form_add_line(
            linenumber=user_properties['number'],
            protocol=user_properties['protocol'],
            device=user_properties.get('device', None),
            context=user_properties['context'],
        )

    form.submit.submit_form()


@step(u'When I rename "([^"]*)" "([^"]*)" to "([^"]*)" "([^"]*)"$')
def when_i_rename_user(step, orig_firstname, orig_lastname, dest_firstname, dest_lastname):
    user_id = user_helper.find_user_id_with_firstname_lastname(orig_firstname, orig_lastname)
    ule_helper.delete_user_line_extension_with_firstname_lastname(dest_firstname, dest_lastname)
    common.open_url('user', 'edit', {'id': user_id})
    user_action_webi.type_user_names(dest_firstname, dest_lastname)
    form.submit.submit_form()


@step(u'When I remove user "([^"]*)" "([^"]*)"$')
def remove_user(step, firstname, lastname):
    world.user_id = user_helper.find_user_id_with_firstname_lastname(firstname, lastname)
    common.open_url('user', 'search', {'search': '%s %s' % (firstname, lastname)})
    common.remove_line('%s %s' % (firstname, lastname))
    common.open_url('user', 'search', {'search': ''})


@step(u'When I search for user "([^"]*)" "([^"]*)"')
def when_i_search_for_user_firstname_lastname(step, firstname, lastname):
    common.open_url('user', 'search', {'search': '%s %s' % (firstname, lastname)})


@step(u'When I search for user with number "([^"]*)"')
def when_i_search_for_user_with_number_group1(step, number):
    common.open_url('user', 'search', {'search': '%s' % number})


@step(u'When I delete agent number "([^"]*)"$')
def when_i_delete_agent_number_1(step, agent_number):
    agent = world.ws.agents.search(agent_number)[0]
    world.ws.agents.delete(agent.id)


@step(u'When I add a user "([^"]*)" "([^"]*)" with a function key with type Customized and extension "([^"]*)"$')
def when_i_add_a_user_group1_group2_with_a_function_key(step, firstname, lastname, extension):
    ule_helper.delete_user_line_extension_with_firstname_lastname(firstname, lastname)
    common.open_url('user', 'add')
    user_action_webi.type_user_names(firstname, lastname)
    user_action_webi.type_func_key('Customized', extension)
    form.submit.submit_form()


@step(u'When I remove line from user "([^"]*)" "([^"]*)" with errors$')
def when_i_remove_line_from_user_1_2_with_errors(step, firstname, lastname):
    _edit_user(firstname, lastname)
    user_action_webi.remove_line()
    form.submit.submit_form_with_errors()


@step(u'When I remove line "([^"]*)" from lines then I see errors$')
def when_i_remove_line_from_lines_then_i_see_errors(step, line_number):
    common.open_url('line')
    line_action_webi.search_line_number(line_number)
    common.remove_line(line_number)
    form.submit.assert_form_errors()
    line_action_webi.unsearch_line()


@step(u'When I add a voicemail "([^"]*)" to the user "([^"]*)" "([^"]*)" with errors$')
def when_i_add_a_voicemail_1_to_the_user_2_3_with_errors(step, voicemail_number, firstname, lastname):
    _edit_user(firstname, lastname)
    user_action_webi.type_voicemail(voicemail_number)
    form.submit.submit_form_with_errors()


@step(u'When I add a voicemail "([^"]*)" to the user "([^"]*)" "([^"]*)"$')
def when_i_add_a_voicemail_1_to_the_user_2_3(step, voicemail_number, firstname, lastname):
    _edit_user(firstname, lastname)
    user_action_webi.type_voicemail(voicemail_number)
    form.submit.submit_form()


@step(u'When I modify the mobile number of user "([^"]*)" "([^"]*)" to "([^"]*)"')
def when_i_modify_the_mobile_number_of_user_1_2_to_3(step, firstname, lastname, mobile_number):
    _edit_user(firstname, lastname)
    user_action_webi.type_mobile_number(mobile_number)
    form.submit.submit_form()


@step(u'When I remove the mobile number of user "([^"]*)" "([^"]*)"')
def when_i_remove_the_mobile_number_of_user_group1_group2(step, firstname, lastname):
    _edit_user(firstname, lastname)
    user_action_webi.type_mobile_number('')
    form.submit.submit_form()


@step(u'Then "([^"]*)" "([^"]*)" is in group "([^"]*)"$')
def then_user_is_in_group(step, firstname, lastname, group_name):
    user_id = user_helper.find_user_id_with_firstname_lastname(firstname, lastname)
    assert user_helper.user_id_is_in_group_name(group_name, user_id)


@step(u'Then I should be at the user list page$')
def then_i_should_be_at_the_user_list_page(step):
    world.browser.find_element_by_id('bc-main', 'User list page not loaded')
    world.browser.find_element_by_name('fm-users-list')


@step(u'When I edit the user "([^"]*)" "([^"]*)" without changing anything')
def when_i_edit_the_user_1_2_without_changing_anything(step, firstname, lastname):
    _edit_user(firstname, lastname)
    form.submit.submit_form()


@step(u'Then I see the user "([^"]*)" "([^"]*)" exists$')
def then_i_see_the_user_group1_group2_exists(step, firstname, lastname):
    common.open_url('user', 'search', {'search': '%s %s' % (firstname, lastname)})
    user_line = common.find_line("%s %s" % (firstname, lastname))
    assert user_line is not None, 'User: %s %s does not exist' % (firstname, lastname)
    common.open_url('user', 'search', {'search': ''})


@step(u'Then the user "([^"]*)" "([^"]*)" not exist')
def then_the_user_not_exist(step, firstname, lastname):
    common.open_url('user', 'search', {'search': '%s %s' % (firstname, lastname)})
    user_line = common.find_line("%s %s" % (firstname, lastname))
    assert user_line is None, 'User: %s %s exist' % (firstname, lastname)
    common.open_url('user', 'search', {'search': ''})


@step(u'Then I see a user with infos:')
def then_i_see_a_user_with_infos(step):
    user_expected_properties = step.hashes[0]
    fullname = user_expected_properties['fullname']
    common.open_url('user', 'search', {'search': '%s' % fullname})
    user_actual_properties = user_action_webi.get_user_list_entry(fullname)
    assert_that(fullname, equal_to(user_expected_properties['fullname']))
    for user_field, user_value in user_expected_properties.iteritems():
        assert_that(user_actual_properties[user_field], equal_to(user_value))
    common.open_url('user', 'search', {'search': ''})


@step(u'Then i see user with username "([^"]*)" "([^"]*)" has a function key with type Customized and extension "([^"]*)"$')
def then_i_see_user_with_username_group1_group2_has_a_function_key(step, firstname, lastname, extension):
    common.open_url('user', 'search', {'search': '%s %s' % (firstname, lastname)})
    common.edit_line("%s %s" % (firstname, lastname))
    common.go_to_tab('Func Keys')
    destination_field = world.browser.find_element_by_id('it-phonefunckey-custom-typeval-0')
    assert destination_field.get_attribute('value') == extension
    type_field = Select(world.browser.find_element_by_id('it-phonefunckey-type-0'))
    assert type_field.first_selected_option.text == "Customized"
    common.open_url('user', 'search', {'search': ''})


@step(u'Then there is no data about this user remaining in the database.$')
def then_there_is_no_data_about_this_user_remaining_in_the_database(step):
    assert user_helper.count_linefeatures(world.user_id) == 0, "Data is remaining in linefeatures after user deletion."
    assert user_helper.count_rightcallmember(world.user_id) == 0, "Data is remaining in rightcallmember after user deletion."
    assert user_helper.count_dialaction(world.user_id) == 0, "Data is remaining in dialaction after user deletion."
    assert user_helper.count_phonefunckey(world.user_id) == 0, "Data is remaining in phonefunckey after user deletion."
    assert user_helper.count_callfiltermember(world.user_id) == 0, "Data is remaining in callfiltermember after user deletion."
    assert user_helper.count_queuemember(world.user_id) == 0, "Data is remaining in queuemember after user deletion."
    assert user_helper.count_schedulepath(world.user_id) == 0, "Data is remaining in schedulepath after user deletion."


@step(u'When I modify the channel type of group "([^"]*)" of user "([^"]*)" to "([^"]*)"')
def when_i_modify_the_channel_type_of_group_group1_of_user_group2_to_group3(step, group, fullname, chantype):
    common.open_url('user', 'search', {'search': fullname})
    common.edit_line(fullname)
    user_action_webi.select_chantype_of_group(group, chantype)
    form.submit.submit_form()


@step(u'Then the channel type of group "([^"]*)" of user "([^"]*)" is "([^"]*)"')
def then_the_channel_type_of_group_group1_of_user_group2_is_group3(step, group, fullname, chantype):
    common.open_url('user', 'search', {'search': fullname})
    common.edit_line(fullname)
    assert_that(user_action_webi.get_chantype_of_group(group), equal_to(chantype))


@step(u'Then "([^"]*)" has enablexfer "([^"]*)"')
def then_user_has_enablexfer_enabled(step, fullname, enabled_string):
    firstname, lastname = fullname.split(' ', 1)
    expected = enabled_string == 'enabled'

    result = user_helper.has_enabled_transfer(firstname, lastname)

    assert_that(result, equal_to(expected), 'Enable transfer for %s' % fullname)


@step(u'Given "([^"]*)" has a dialaction on "([^"]*)" to "([^"]*)" "([^"]*)"')
def given_user_has_a_dialaction(step, fullname, event, dialaction, destination):
    _edit_user(*fullname.split(' ', 1))
    common.go_to_tab('No answer')

    if event == 'No answer':
        action_type = 'noanswer'
    elif event == 'Busy':
        action_type = 'busy'
    else:
        raise NotImplementedError('%s dialaction is not implemented' % event)

    if dialaction != 'User':
        raise NotImplementedError('%s dialaction destination is not implemented' % destination)

    action_type_id = 'it-dialaction-%s-actiontype' % action_type
    action_destination_id = 'it-dialaction-%s-user-actionarg1' % action_type

    _select(action_type_id, dialaction)
    _select(action_destination_id, destination)

    form.submit.submit_form()


@step(u'Given "([^"]*)" has a "([^"]*)" ringing time')
def given_user_has_a_n_ringing_time(step, fullname, delay_string):
    _edit_user(*fullname.split(' ', 1))

    _select('it-userfeatures-ringseconds', delay_string)

    form.submit.submit_form()


def _select(id_, text):
    form.select.set_select_field_with_id(id_, text)


def _edit_user(firstname, lastname):
    user_id = user_helper.find_user_id_with_firstname_lastname(firstname, lastname)
    common.open_url('user', 'edit', qry={'id': user_id})
