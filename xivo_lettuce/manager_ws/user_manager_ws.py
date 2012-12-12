# -*- coding: utf-8 -*-

import voicemail_manager_ws
from lettuce import world
from xivo_ws import User, UserLine, UserVoicemail
from xivo_lettuce.exception import NoSuchProfileException
from xivo_lettuce.manager_ws import group_manager_ws


def add_user(data_dict):
    user = User()
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

    if 'line_number' in data_dict and 'line_context' in data_dict:
        user.line = UserLine()
        user.line.number = data_dict['line_number']
        user.line.context = data_dict['line_context']

    if 'voicemail_name' in data_dict and 'voicemail_number' in data_dict:
        user.voicemail = UserVoicemail()
        user.voicemail.name = data_dict['voicemail_name']
        user.voicemail.number = data_dict['voicemail_number']

    ret = world.ws.users.add(user)
    if not ret:
        return False

    return int(ret)


def add_or_replace_user(data_dict):
    firstname = data_dict['firstname']
    lastname = data_dict.get('lastname', '')
    delete_users_with_firstname_lastname(firstname, lastname)

    if 'line_number' in data_dict:
        number = data_dict['line_number']
        context = data_dict.get('line_context', 'default')
        delete_users_with_number(number, context)

    return add_user(data_dict)


def delete_users_with_number(number, context):
    user_ids = search_user_ids_with_number(number, context)
    for user_id in user_ids:
        _delete_user_with_id(user_id)


def delete_users_with_firstname_lastname(firstname, lastname):
    users = _search_users_with_firstname_lastname(firstname, lastname)
    for user in users:
        _delete_user(user)


def delete_users_with_firstname(firstname):
    users = world.ws.users.search(firstname)
    for user in users:
        _delete_user(user)


def delete_users_with_profile(profile_name):
    users = world.ws.users.list()
    profiles = [profile for profile in world.ws.cti_profiles.list() if profile.name == profile_name]

    if not profiles:
        raise NoSuchProfileException('The CTI profile %s does not exist.' % profile_name)

    profile_id = profiles[0].id
    for user in users:
        if user.client_profile_id == profile_id:
            _delete_user(user)


def _delete_user_with_id(user_id):
    world.ws.users.delete(user_id)


def _delete_user(user):
    if user.voicemail:
        voicemail_manager_ws.delete_voicemail_with_id(user.voicemail.id)
    world.ws.users.delete(user.id)


def is_user_with_name_exists(firstname, lastname):
    users = _search_users_with_firstname_lastname(firstname, lastname)
    return bool(users)


def find_user_with_firstname_lastname(firstname, lastname):
    users = _search_users_with_firstname_lastname(firstname, lastname)
    if len(users) != 1:
        raise Exception('expecting 1 user with name %r %r; found %s' %
                        (firstname, lastname, len(users)))
    return users[0]


def find_user_id_with_firstname_lastname(firstname, lastname):
    user = find_user_with_firstname_lastname(firstname, lastname)
    return user.id


def _search_users_with_firstname_lastname(firstname, lastname):
    users = world.ws.users.search('%s %s' % (firstname, lastname))
    return [user for user in users if
            user.firstname == firstname and
            user.lastname == lastname]


def search_user_ids_with_number(number, context):
    lines = world.ws.lines.search_by_number(number)
    return [line.user_id for line in lines if line.context == context]


def user_id_is_in_group_name(group_name, user_id):
    group = group_manager_ws.get_group_with_name(group_name)
    for id in group.user_ids:
        if id == user_id:
            return True
    return False


def disable_cti_client(firstname, lastname):
    user = find_user_with_firstname_lastname(firstname, lastname)
    user.enable_client = False
    world.ws.users.edit(user)


def enable_cti_client(firstname, lastname):
    user = find_user_with_firstname_lastname(firstname, lastname)
    user.client_username = firstname.lower()
    user.client_password = lastname.lower()
    user.enable_client = True
    world.ws.users.edit(user)
