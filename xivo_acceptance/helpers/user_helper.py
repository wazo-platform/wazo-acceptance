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

from xivo_acceptance.helpers import voicemail_helper, group_helper, provd_helper
from xivo_dao.data_handler.user import dao as user_dao
from xivo_dao.data_handler.user import services as user_services
from xivo_dao.data_handler.exception import ElementNotExistsError
from xivo_lettuce import postgres
from xivo_lettuce.exception import NoSuchProfileException
from xivo_lettuce.remote_py_cmd import remote_exec
from xivo_ws import User, UserLine, UserVoicemail
from xivo_ws.exception import WebServiceRequestError


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


def find_user_with_firstname_lastname(firstname, lastname):
    user = find_by_firstname_lastname(firstname, lastname)
    if user is None:
        raise Exception('expecting user with name %r %r; not found' % (firstname, lastname))
    return user


def find_user_id_with_firstname_lastname(firstname, lastname):
    user = find_user_with_firstname_lastname(firstname, lastname)
    return user.id


def find_user_by_name(name):
    firstname, lastname = name.split(" ")
    return user_dao.find_user(firstname, lastname)


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


def delete_user_line_extension_voicemail(firstname, lastname, context=None, exten=None, mailbox=None):
    if exten and context:
        delete_user_line_extension_with_exten_context(exten, context)
    if mailbox and context:
        voicemail_helper.delete_voicemail_with_number_context(mailbox, context)
    delete_user_line_extension_with_firstname_lastname(firstname, lastname)
    delete_all_user_with_firstname_lastname(firstname, lastname)


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


def delete_user_line_extension_with_firstname_lastname(firstname, lastname):
    try:
        remote_exec(_delete_user_line_extension_with_firstname_lastname, firstname=firstname, lastname=lastname)
    except RemoteError:
        pass


def _delete_user_line_extension_with_firstname_lastname(channel, firstname, lastname):
    from xivo_dao.data_handler.user import services as user_services
    from xivo_dao.data_handler.user_line_extension import services as ule_services

    fullname = '%s %s' % (firstname, lastname)
    users = user_services.find_all_by_fullname(fullname)

    for user in users:
        ules = ule_services.find_all_by_user_id(user.id)
        if ules:
            for ule in ules:
                ule_services.delete_everything(ule)
        else:
            user_services.delete(user)


def delete_user_line_extension_with_user_id(user_id):
    try:
        remote_exec(_delete_user_line_extension_with_user_id, user_id=user_id)
    except RemoteError:
        pass


def _delete_user_line_extension_with_user_id(channel, user_id):
    from xivo_dao.data_handler.user import services as user_services
    from xivo_dao.data_handler.user_line_extension import services as ule_services

    ules = ule_services.find_all_by_user_id(user_id)

    if ules:
        for ule in ules:
            ule_services.delete_everything(ule)
    else:
        user = user_services.get(user_id)
        user_services.delete(user)


def delete_user_line_extension_with_exten_context(exten, context):
    try:
        remote_exec(_delete_user_line_extension_with_number_context, exten=exten, context=context)
    except RemoteError:
        pass


def _delete_user_line_extension_with_number_context(channel, exten, context):
    from xivo_dao.data_handler.extension import services as extension_services
    from xivo_dao.data_handler.user_line_extension import services as ule_services

    try:
        extension = extension_services.get_by_exten_context(exten, context)
    except LookupError:
        return

    ules = ule_services.find_all_by_extension_id(extension.id)

    if ules:
        for ule in ules:
            ule_services.delete_everything(ule)
    else:
        extension_services.delete(extension)


def delete_all():
    remote_exec(_delete_all)


def _delete_all(channel):
    from xivo_dao.data_handler.user import services as user_services
    from xivo_dao.data_handler.line import services as line_services
    from xivo_dao.data_handler.extension import services as extension_services
    from xivo_dao.data_handler.user_line_extension import dao as ule_dao
    from xivo_dao.data_handler.exception import ElementDeletionError
    from xivo_dao.data_handler.exception import ElementNotExistsError

    for user in user_services.find_all():

        ules = ule_dao.find_all_by_user_id(user.id)
        for ule in ules:
            try:
                ule_dao.delete(ule)
            except (ElementDeletionError, ElementNotExistsError):
                pass

            try:
                line = line_services.get(ule.line_id)
                line_services.delete(line)
            except (ElementDeletionError, ElementNotExistsError):
                pass

            if ule.extension_id:
                try:
                    extension = extension_services.get(ule.extension_id)
                    extension_services.delete(extension)
                except (ElementDeletionError, ElementNotExistsError):
                    pass

        try:
            user_services.delete(user)
        except (ElementDeletionError, ElementNotExistsError):
            pass

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


def add_or_replace_user(data_dict):
    firstname = data_dict['firstname']
    lastname = data_dict.get('lastname', '')
    mailbox = data_dict.get('voicemail_number', None)
    exten = data_dict.get('line_number', None)
    context = data_dict.get('line_context', None)

    delete_user_line_extension_voicemail(firstname,
                                         lastname,
                                         exten=exten,
                                         context=context,
                                         mailbox=mailbox)

    return add_user(data_dict)


def delete_users_with_profile(profile_name):
    users = world.ws.users.list()
    profiles = [profile for profile in world.ws.cti_profiles.list() if profile.name == profile_name]

    if not profiles:
        raise NoSuchProfileException('The CTI profile %s does not exist.' % profile_name)

    profile_id = profiles[0].id
    for user in users:
        if user.client_profile_id == profile_id:
            if user.voicemail:
                voicemail_helper.delete_voicemail_with_user_id(user.id)
            delete_user_line_extension_with_user_id(user.id)


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
