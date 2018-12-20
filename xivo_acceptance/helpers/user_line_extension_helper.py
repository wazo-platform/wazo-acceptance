# -*- coding: utf-8 -*-
# Copyright (C) 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from lettuce import world

from xivo_acceptance.helpers import (
    extension_helper,
    line_write_helper,
    user_helper,
    voicemail_helper,
)


def delete_user_line_extension_voicemail(
        firstname,
        lastname,
        context=None,
        exten=None,
        mailbox=None,
        username=None
):
    if mailbox and context:
        delete_voicemail(mailbox, context)
    if exten and context:
        delete_extension(exten, context)
        delete_lines(exten)

    if username:
        user = user_helper.find_by_username(username)
        if user:
            delete_lines_for_user(user['uuid'])
            delete_user(user['uuid'])

    user = user_helper.find_by_firstname_lastname(firstname, lastname)
    if user:
        delete_lines_for_user(user['id'])
        delete_user(user['id'])


def delete_voicemail(mailbox, context):
    voicemail_helper.delete_similar_voicemails({'number': mailbox, 'context': context})


def delete_extension(exten, context):
    extension_helper.delete_similar_extensions({'exten': exten, 'context': context})


def delete_lines(exten):
    line_write_helper.delete_similar_lines(exten)


def delete_lines_for_user(user_id):
    user = world.confd_client.users.get(user_id)
    for line in user['lines']:
        line_write_helper.delete_line(line['id'])


def delete_user(user_id):
    user_helper.delete_user(user_id)


def add_or_replace_user(data_dict, step=None):
    firstname = data_dict['firstname']
    lastname = data_dict.get('lastname', '')
    mailbox = data_dict.get('voicemail_number', None)
    exten = data_dict.get('line_number', None)
    context = data_dict.get('line_context', None)
    username = data_dict.get('client_username', None)

    delete_user_line_extension_voicemail(
        firstname,
        lastname,
        exten=exten,
        context=context,
        mailbox=mailbox,
        username=username,
    )

    return user_helper.add_user(data_dict, step=step)


def delete_users_with_profile(profile_name):
    users = world.confd_client.users.list()['items']
    for user in users:
        if user['cti_profile'] and user['cti_profile']['name'] == profile_name:
            if user['voicemail']:
                voicemail_helper.delete_voicemail(user['voicemail']['id'])
            delete_lines_for_user(user['id'])
            delete_user(user['id'])
