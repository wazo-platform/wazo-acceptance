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

from lettuce import world
from execnet.gateway_base import RemoteError

from xivo_acceptance.helpers import group_helper, provd_helper, line_helper, voicemail_helper, func_key_helper, \
    entity_helper
from xivo_dao.data_handler.user import dao as user_dao
from xivo_dao.data_handler.user import services as user_services
from xivo_dao.data_handler.exception import ElementNotExistsError
from xivo_lettuce import postgres
from xivo_lettuce.remote_py_cmd import remote_exec, remote_exec_with_result
from xivo_ws import User, UserLine, UserVoicemail
from xivo_ws.exception import WebServiceRequestError


def add_or_replace_user(userinfo):
    delete_similar_users(userinfo)
    create_user(userinfo)


def get_by_user_id(user_id):
    try:
        user = user_services.get(user_id)
    except ElementNotExistsError:
        return None
    return user


def get_by_exten_context(exten, context):
    try:
        user = user_services.get_by_number_context(exten, context)
    except ElementNotExistsError:
        return None
    return user


def find_by_firstname_lastname(firstname, lastname):
    return user_services.find_by_firstname_lastname(firstname, lastname)


def get_by_firstname_lastname(firstname, lastname):
    user = find_by_firstname_lastname(firstname, lastname)
    if user is None:
        raise Exception('expecting user with name %r %r; not found' % (firstname, lastname))
    return user


def find_user_id_with_firstname_lastname(firstname, lastname):
    user = get_by_firstname_lastname(firstname, lastname)
    return user.id


def find_user_by_name(name):
    firstname, lastname = name.split(" ")
    return user_dao.find_user(firstname, lastname)


def find_line_id_for_user(user_id):
    return remote_exec_with_result(_find_line_id_for_user, user_id=user_id)


def _find_line_id_for_user(channel, user_id):
    from xivo_dao.data_handler.user_line import services as user_line_services
    user_lines = user_line_services.find_all_by_user_id(user_id)

    if len(user_lines) > 0:
        channel.send(user_lines[0].line_id)
    else:
        channel.send(None)


def is_user_with_name_exists(firstname, lastname):
    user = user_services.find_by_firstname_lastname(firstname, lastname)
    if user is None:
        return False
    return True


def create_user(userinfo):
    remote_exec(_create_user, userinfo=userinfo)


def _create_user(channel, userinfo):
    from xivo_dao.data_handler.user import services as user_services
    from xivo_dao.data_handler.user.model import User

    user = User(**userinfo)
    user_services.create(user)


def delete_similar_users(userinfo):
    if 'id' in userinfo:
        delete_user(int(userinfo['id']))

    if 'firstname' in userinfo and 'lastname' in userinfo:
        user = find_by_firstname_lastname(userinfo['firstname'], userinfo['lastname'])
        if user:
            delete_user(user.id)


def delete_all_user_with_firstname_lastname(firstname, lastname):
    try:
        remote_exec(_delete_all_user_with_firstname_lastname, firstname=firstname, lastname=lastname)
    except RemoteError:
        pass


def _delete_all_user_with_firstname_lastname(channel, firstname, lastname):
    from xivo_dao.data_handler.user import services as user_services

    fullname = '%s %s' % (firstname, lastname)
    users = user_services.find_all_by_fullname(fullname)

    if users:
        for user in users:
            user_services.delete(user)


def delete_with_user_id(user_id):
    try:
        remote_exec(_delete_with_user_id, user_id=user_id)
    except RemoteError:
        pass


def _delete_with_user_id(channel, user_id):
    from xivo_dao.data_handler.user import services as user_services

    user = user_services.get(user_id)

    if user:
        user_services.delete(user)


def delete_user_with_firstname_lastname(firstname, lastname):
    try:
        remote_exec(_delete_user_with_firstname_lastname, firstname=firstname, lastname=lastname)
    except RemoteError:
        pass


def _delete_user_with_firstname_lastname(channel, firstname, lastname):
    from xivo_dao.data_handler.user import services as user_services

    user = user_services.find_by_firstname_lastname(firstname, lastname)

    if user:
        user_services.delete(user)


def delete_all():
    user_ids = remote_exec_with_result(_all_user_ids)
    for user_id in user_ids:
        delete_user(user_id)


def _all_user_ids(channel):
    from xivo_dao.data_handler.user import services as user_services

    user_ids = [u.id for u in user_services.find_all()]
    channel.send(user_ids)


def delete_user(user_id):
    if get_by_user_id(user_id):
        _delete_line_associations(user_id)
        _delete_voicemail_associations(user_id)
        _delete_func_key_associations(user_id)

        template_id = func_key_helper.find_template_for_user(user_id)
        remote_exec(_delete_using_user_service, user_id=user_id)
        func_key_helper.delete_template_and_func_keys(template_id)


def _delete_line_associations(user_id):
    line_id = find_line_id_for_user(user_id)
    if line_id:
        line_helper.delete_line_associations(line_id)


def _delete_voicemail_associations(user_id):
    voicemail_helper.delete_voicemail_with_user_id(user_id)


def _delete_func_key_associations(user_id):
    func_key_helper.delete_func_keys_with_user_destination(user_id)


def _delete_using_user_service(channel, user_id):
    from xivo_dao.data_handler.user import services as user_services

    user = user_services.get(user_id)
    user_services.delete(user)


'''
    #TODO refactor to use dao
'''


def add_user(data_dict):
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

    if 'line_number' in data_dict and 'line_context' in data_dict:
        user.line = UserLine()
        user.line.number = data_dict['line_number']
        user.line.context = data_dict['line_context']
        if 'protocol' in data_dict:
            user.line.protocol = data_dict['protocol']
        if 'device' in data_dict:
            device = provd_helper.find_by_mac(data_dict['device'])
            device_id = str(device['id'])
            user.line.device_id = device_id

    if 'voicemail_name' in data_dict and 'voicemail_number' in data_dict:
        user.voicemail = UserVoicemail()
        user.voicemail.name = data_dict['voicemail_name']
        user.voicemail.number = data_dict['voicemail_number']

    if 'mobile_number' in data_dict:
        user.mobile_number = data_dict['mobile_number']

    try:
        ret = world.ws.users.add(user)
    except WebServiceRequestError as e:
        raise Exception('Could not add user %s %s: %s' % (user.firstname, user.lastname, e))
    if not ret:
        return False

    return int(ret)


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
