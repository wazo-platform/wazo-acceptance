# -*- coding: utf-8 -*-

import voicemail_manager_ws
from lettuce.registry import world
from xivo_ws.objects.user import User, UserLine, UserVoicemail
from xivo_lettuce.manager_ws import line_manager_ws, group_manager_ws


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


def delete_user_with_firstname_lastname(firstname, lastname):
    users = world.ws.users.search('%s %s' % (firstname, lastname))
    for user in users:
        if user.voicemail:
            voicemail_manager_ws.delete_voicemail_with_id(user.voicemail.id)
        if user.line:
            line_manager_ws.delete_line_with_number(user.line.number)
        world.ws.users.delete(user.id)


def delete_user_with_firstname(firstname):
    users = world.ws.users.search(firstname)
    for user in users:
        if user.voicemail:
            voicemail_manager_ws.delete_voicemail_with_id(user.voicemail.id)
        if user.line:
            line_manager_ws.delete_line_with_number(user.line.number)
        world.ws.users.delete(user.id)


def delete_users_with_profile(profile):
    users = world.ws.users.list()
    for user in users:
        if user.client_profile == profile:
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


def user_id_is_in_group_name(group_name, user_id):
    try:
        group_id = group_manager_ws.get_group_id_with_name(group_name)
    except Exception:
        return False
    else:
        group = group_manager_ws.get_group_with_id(group_id)
        for id in group.user_ids:
            if id == user_id:
                return True
    return False
