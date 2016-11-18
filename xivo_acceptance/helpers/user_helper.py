# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
# Copyright (C) 2016 Proformatique Inc.
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
from requests.exceptions import HTTPError

from xivo_acceptance import helpers
from xivo_acceptance.helpers import group_helper
from xivo_acceptance.helpers import line_write_helper
from xivo_acceptance.helpers import line_read_helper
from xivo_acceptance.helpers import voicemail_helper
from xivo_acceptance.helpers import entity_helper
from xivo_acceptance.helpers import sip_config
from xivo_acceptance.helpers import sip_phone
from xivo_acceptance.lettuce import postgres
from xivo_acceptance.action.webi import user as user_action_webi
from xivo_ws import User
from xivo_ws.exception import WebServiceRequestError


def add_or_replace_user(userinfo):
    delete_similar_users(userinfo)
    world.confd_client.users.create(userinfo)


def find_by_user_id(user_id):
    try:
        return world.confd_client.users.get(user_id)
    except HTTPError:
        return None


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
    users = world.confd_client.users.list(firstname=firstname, lastname=lastname)['items']
    if not users:
        return None
    return users[0]


def get_by_firstname_lastname(firstname, lastname):
    user = find_by_firstname_lastname(firstname, lastname)
    assert_that(user, is_not(none()),
                (u"user '%s %s' does not exist" % (firstname, lastname)).encode('utf8'))
    return user


def get_user_by_name(name):
    firstname, lastname = name.split(" ", 1)
    return get_by_firstname_lastname(firstname, lastname)


def delete_similar_users(userinfo):
    if 'firstname' in userinfo and 'lastname' in userinfo:
        user = find_by_firstname_lastname(userinfo['firstname'],
                                          userinfo['lastname'])
        if user:
            delete_user(user['id'])


def delete_user(user_id):
    user = world.confd_client.users.get(user_id)
    _delete_voicemail(user)
    _delete_line_associations(user)
    _delete_user(user)


def _delete_line_associations(user):
    for line in user['lines']:
        line = world.confd_client.lines.get(line['id'])
        line_write_helper.dissociate_device(line)
        line_write_helper.dissociate_users(line)


def _delete_voicemail(user):
    voicemail = voicemail_helper.find_voicemail_by_user_id(user['id'])
    if voicemail:
        voicemail_helper.delete_voicemail(voicemail['id'])


def _delete_user(user):
    world.confd_client.users.delete(user['id'])


def add_user_with_infos(user_data, step=None):
    user_ws_data = {}
    user_ws_data['firstname'] = user_data['firstname']
    user_ws_data['lastname'] = user_data['lastname']

    if user_data.get('entity_name'):
        user_ws_data['entity_name'] = user_data.get('entity_name', 'xivoentity')

    if user_data.get('number') and user_data.get('context'):
        user_ws_data['line_number'] = user_data['number']
        user_ws_data['line_context'] = user_data['context']
        if 'protocol' in user_data:
            user_ws_data['protocol'] = user_data['protocol']
        if 'device' in user_data:
            user_ws_data['device'] = user_data['device']
        if 'device_slot' in user_data:
            user_ws_data['device_slot'] = user_data['device_slot']

        if {'voicemail_name', 'voicemail_number', 'voicemail_context'}.issubset(user_data):
            user_ws_data['voicemail_name'] = user_data['voicemail_name']
            user_ws_data['voicemail_number'] = user_data['voicemail_number']
            user_ws_data['voicemail_context'] = user_data['voicemail_context']

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

    user_id = helpers.user_line_extension_helper.add_or_replace_user(user_ws_data, step=step)

    schedule = user_data.get('schedule')
    if schedule:
        fullname = '{firstname} {lastname}'.format(**user_data).strip()
        user_action_webi.add_schedule(fullname, schedule)

    if user_data.get('agent_number'):
        helpers.agent_helper.delete_agents_with_number(user_data['agent_number'])
        agent_data = {'firstname': user_data['firstname'],
                      'lastname': user_data['lastname'],
                      'number': user_data['agent_number'],
                      'context': user_data.get('context', 'default'),
                      'users': [int(user_id)]}
        helpers.agent_helper.add_agent(agent_data)

    if user_data.get('group_name'):
        user = world.confd_client.users.get(user_id)
        group_helper.add_or_replace_group(user_data['group_name'], users=[user])


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
            user.entity_id = entity['id']
    else:
        user.entity_id = entity_helper.default_entity_id()

    if 'mobile_number' in data_dict:
        user.mobile_number = data_dict['mobile_number']

    try:
        user_id = world.ws.users.add(user)
    except WebServiceRequestError as e:
        raise Exception('Could not add user %s %s: %s' % (user.firstname, user.lastname, e))
    if not user_id:
        return False

    if 'line_number' in data_dict and 'line_context' in data_dict:
        extension_data = {'context': data_dict['line_context'],
                          'exten': data_dict['line_number']}
        extension = world.confd_client.extensions.create(extension_data)
        line_data = {
            'context': data_dict['line_context'],
        }
        if 'device_slot' in data_dict:
            line_data['position'] = data_dict['device_slot']
        line = world.confd_client.lines.create(line_data)

        protocol = data_dict.get('protocol', 'sip')
        if protocol == 'sip':
            endpoint = world.confd_client.endpoints_sip.create({})
            world.confd_client.lines(line['id']).add_endpoint_sip(endpoint)
        elif protocol == 'sccp':
            endpoint = world.confd_client.endpoints_sccp.create({})
            world.confd_client.lines(line['id']).add_endpoint_sccp(endpoint)
        elif protocol == 'custom':
            endpoint = world.confd_client.endpoints_custom.create({})
            world.confd_client.lines(line['id']).add_endpoint_custom(endpoint)

        world.confd_client.lines(line['id']).add_extension(extension)
        world.confd_client.users(user_id).add_line(line['id'])

        mac = data_dict.get('device')
        if mac:
            device = world.confd_client.devices.list(mac=mac)['items'][0]
            world.confd_client.lines(line['id']).add_device(device['id'])

    if {'voicemail_name', 'voicemail_number', 'voicemail_context'}.issubset(data_dict):
        voicemail = voicemail_helper.add_or_replace_voicemail({
            'name': data_dict['voicemail_name'],
            'number': data_dict['voicemail_number'],
            'context': data_dict['voicemail_context'],
        })
        world.confd_client.users.relations(user_id).add_voicemail(voicemail)

    if step is not None:
        _register_and_track_phone(step.scenario, data_dict)

    return int(user_id)


def _register_and_track_phone(scenario, user_data):
    phone_available = user_data.get('protocol') == 'sip' and 'line_number' in user_data
    if not phone_available:
        return

    number = user_data['line_number']
    context = user_data.get('line_context', 'default')
    line = line_read_helper.find_with_exten_context(number, context)
    if not line or not line['endpoint_sip']:
        return

    name = ('%s %s' % (user_data.get('firstname', ''),
                       user_data.get('lastname', ''))).strip()

    endpoint_sip = world.confd_client.endpoints_sip.get(line['endpoint_sip']['id'])
    phone_config = sip_config.create_config(world.config, scenario.phone_register, endpoint_sip)
    phone = sip_phone.register_line(phone_config)
    if phone:
        scenario.phone_register.add_registered_phone(phone, name)


def user_is_in_group(user, group):
    for group_user in group['members']['users']:
        if user['uuid'] == group_user['uuid']:
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


def get_unconditional_forward(fullname):
    firstname, lastname = fullname.split(' ', 1)
    query = """
    SELECT
        enableunc,
        destunc
    FROM
        userfeatures
    WHERE
        firstname = :firstname
        AND lastname = :lastname
    """

    rows = postgres.exec_sql_request(query, firstname=firstname, lastname=lastname).fetchall()
    if len(rows) != 1:
        raise Exception('expected 1 user "{} {}": got {}'.format(firstname, lastname, len(rows)))

    enabled, dest = rows[0]
    return bool(enabled), dest
