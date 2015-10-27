# -*- coding: utf-8 -*-

# Copyright (C) 2013-2015 Avencall
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

from lettuce import world
from hamcrest import assert_that, is_not, none

from xivo_acceptance.helpers import group_helper
from xivo_acceptance.helpers import provd_helper
from xivo_acceptance.helpers import line_write_helper
from xivo_acceptance.helpers import line_sip_helper
from xivo_acceptance.helpers import voicemail_helper
from xivo_acceptance.helpers import func_key_helper
from xivo_acceptance.helpers import entity_helper
from xivo_acceptance.helpers import sip_config
from xivo_acceptance.helpers import sip_phone
from xivo_acceptance.lettuce import postgres
from xivo_acceptance.action.confd import user_action_confd as user_action
from xivo_acceptance.action.confd import user_line_action_confd as user_line_action
from xivo_ws import User, UserLine, UserVoicemail
from xivo_ws.exception import WebServiceRequestError


def add_or_replace_user(userinfo):
    delete_similar_users(userinfo)
    return create_user(userinfo)


def find_by_user_id(user_id):
    response = user_action.get_user(user_id)
    return response.resource() if response.status_ok() else None


def get_by_exten_context(exten, context):
    user = find_by_exten_context(exten, context)
    assert_that(user, is_not(none()),
                "User with exten %s@%s not found" % (exten, context))
    return user


def find_by_exten_context(exten, context):
    query = """
    SELECT
        CAST(typeval AS INT)
    FROM
        extensions
    WHERE
        type = 'user'
        AND exten = :exten
        AND context = :context
        AND typeval != '0'
    """

    result = postgres.exec_sql_request(query, exten=exten, context=context)
    user_id = result.scalar()
    return find_by_user_id(user_id) if user_id else None


def find_by_firstname_lastname(firstname, lastname):
    fullname = "%s %s" % (firstname, lastname)
    response = user_action.user_search(fullname)
    users = [user
             for user in response.items()
             if user['firstname'] == firstname and user['lastname'] == lastname]
    return users[0] if users else None


def get_by_firstname_lastname(firstname, lastname):
    user = find_by_firstname_lastname(firstname, lastname)
    assert_that(user, is_not(none()),
                (u"user '%s %s' does not exist" % (firstname, lastname)).encode('utf8'))
    return user


def get_user_id_with_firstname_lastname(firstname, lastname):
    user = get_by_firstname_lastname(firstname, lastname)
    return user['id']


def get_user_by_name(name):
    firstname, lastname = name.split(" ", 1)
    return get_by_firstname_lastname(firstname, lastname)


def find_line_id_for_user(user_id):
    response = user_line_action.get_user_line(user_id)
    items = response.items()
    return items[0]['line_id'] if items else None


def get_line_id_for_user(user_id):
    line_id = find_line_id_for_user(user_id)
    assert_that(line_id, is_not(none()),
                "User %s has no lines" % user_id)
    return line_id


def user_lines_for_user(user_id):
    response = user_line_action.get_user_line(user_id)
    return response.items()


def find_agent_id_for_user(user_id):
    query = 'select agentid from userfeatures where id = {user_id}'.format(user_id=user_id)
    return postgres.exec_sql_request(query).scalar()


def create_user(userinfo):
    user = dict(userinfo)
    if 'id' in user:
        user['id'] = int(user['id'])
    response = user_action.create_user(user)
    return response.resource()


def delete_similar_users(userinfo):
    if 'id' in userinfo:
        delete_user(userinfo['id'])
    if 'firstname' in userinfo and 'lastname' in userinfo:
        user = find_by_firstname_lastname(userinfo['firstname'],
                                          userinfo['lastname'])
        if user:
            delete_user(user['id'])


def delete_user(user_id):
    if find_by_user_id(user_id):
        _delete_voicemail_associations(user_id)
        _delete_line_associations(user_id)
        _delete_func_key_associations(user_id)

        template_id = func_key_helper.find_template_for_user(user_id)
        _delete_user(user_id)
        func_key_helper.delete_template_and_func_keys(template_id)


def _delete_line_associations(user_id):
    user_lines = user_lines_for_user(user_id)
    main = [ul for ul in user_lines if ul['main_user']]
    secondary = [ul for ul in user_lines if not ul['main_user']]
    for ul in (secondary + main):
        line_write_helper.dissociate_device(ul['line_id'])
        line_write_helper.dissociate_users(ul['line_id'])


def _delete_voicemail_associations(user_id):
    voicemail = voicemail_helper.find_voicemail_by_user_id(user_id)
    if voicemail:
        voicemail_helper.delete_voicemail(voicemail['id'])


def _delete_func_key_associations(user_id):
    func_key_helper.delete_func_keys_with_user_destination(user_id)


def _delete_user(user_id):
    response = user_action.delete_user(user_id)
    response.check_status()


def add_user(data_dict, step=None):
    user = User()

    if 'id' in data_dict:
        user.id = data_dict['id']

    user.firstname = data_dict['firstname']

    if 'lastname' in data_dict:
        user.lastname = data_dict['lastname']
    if 'agentid' in data_dict:
        user.agent_id = int(data_dict['agentid'])
    if 'language' in data_dict:
        user.language = data_dict['language']
    if 'enable_client' in data_dict:
        user.enable_client = bool(data_dict['enable_client'])
    if 'client_username' in data_dict:
        user.client_username = data_dict['client_username']
    if 'client_password' in data_dict:
        user.client_password = data_dict['client_password']
    if 'client_profile' in data_dict:
        user.client_profile = data_dict['client_profile']
    if 'bsfilter' in data_dict:
        user.bsfilter = data_dict['bsfilter']

    if 'entity_name' in data_dict:
        entity = entity_helper.get_entity_with_name(data_dict['entity_name'])
        if entity:
            user.entity_id = entity.id
    else:
        user.entity_id = entity_helper.oldest_entity_id()

    if 'line_number' in data_dict and 'line_context' in data_dict:
        user.line = UserLine()
        user.line.number = data_dict['line_number']
        user.line.context = data_dict['line_context']
        if 'protocol' in data_dict:
            user.line.protocol = data_dict['protocol']
        if 'device' in data_dict:
            device = provd_helper.find_by_mac(data_dict['device'])
            if device is not None:
                user.line.device_id = str(device['id'])
        if 'device_slot' in data_dict:
            user.line.device_slot = int(data_dict['device_slot'])

    if {'voicemail_name', 'voicemail_number', 'voicemail_context'}.issubset(data_dict):
        user.voicemail = UserVoicemail()
        user.voicemail.name = data_dict['voicemail_name']
        user.voicemail.number = data_dict['voicemail_number']
        user.voicemail.context = data_dict['voicemail_context']

    if 'mobile_number' in data_dict:
        user.mobile_number = data_dict['mobile_number']

    try:
        ret = world.ws.users.add(user)
    except WebServiceRequestError as e:
        raise Exception('Could not add user %s %s: %s' % (user.firstname, user.lastname, e))
    if not ret:
        return False

    if step is not None:
        _register_and_track_phone(step.scenario, data_dict)

    return int(ret)


def _register_and_track_phone(scenario, user_data):
    phone_available = user_data.get('protocol') == 'sip' and 'line_number' in user_data
    if not phone_available:
        return

    number = user_data['line_number']
    context = user_data.get('line_context', 'default')
    line = line_sip_helper.find_with_exten_context(number, context)
    if not line:
        return

    name = ('%s %s' % (user_data.get('firstname', ''),
                       user_data.get('lastname', ''))).strip()

    phone_config = sip_config.create_config(world.config, scenario.phone_register, line)
    phone = sip_phone.register_line(phone_config)
    if phone:
        scenario.phone_register.add_registered_phone(phone, name)


def user_id_is_in_group_name(group_name, user_id):
    group = group_helper.get_group_with_name(group_name)
    for id in group.user_ids:
        if id == user_id:
            return True
    return False


def disable_cti_client(firstname, lastname):
    users = _search_users_with_firstname_lastname(firstname, lastname)
    for user in users:
        user.enable_client = False
        world.ws.users.edit(user)


def enable_cti_client(firstname, lastname):
    users = _search_users_with_firstname_lastname(firstname, lastname)
    for user in users:
        user.enable_client = True
        world.ws.users.edit(user)


def has_enabled_transfer(firstname, lastname):
    for user in _search_users_with_firstname_lastname(firstname, lastname):
        return user.enable_transfer
    return False


def _search_users_with_firstname_lastname(firstname, lastname):
    users = world.ws.users.search('%s %s' % (firstname, lastname))
    return [user for user in users if
            user.firstname == firstname and
            user.lastname == lastname]


def count_linefeatures(user_id):
    return _count_table_with_cond("user_line", {'"user_id"': user_id})


def count_rightcallmember(user_id):
    return _count_table_with_cond("rightcallmember", {'"type"': "'user'", '"typeval"': "'%s'" % user_id})


def count_dialaction(user_id):
    return _count_table_with_cond("dialaction", {'"category"': "'user'", '"categoryval"': "'%s'" % user_id})


def count_phonefunckey(user_id):
    return _count_table_with_cond("phonefunckey", {'"iduserfeatures"': user_id})


def count_callfiltermember(user_id):
    return _count_table_with_cond("callfiltermember", {'"type"': "'user'", '"typeval"': "'%s'" % user_id})


def count_queuemember(user_id):
    return _count_table_with_cond("queuemember", {'"usertype"': "'user'", '"userid"': user_id})


def count_schedulepath(user_id):
    return _count_table_with_cond("schedule_path", {'"path"': "'user'", '"pathid"': user_id})


def _count_table_with_cond(table, cond_dict):
    return postgres.exec_count_request(table, **cond_dict)
