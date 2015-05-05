# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

from xivo_acceptance.helpers import user_helper, voicemail_helper, line_helper, extension_helper
from xivo_acceptance.lettuce.exception import NoSuchProfileException


def delete_user_line_extension_voicemail(firstname, lastname, context=None, exten=None, mailbox=None):
    if mailbox and context:
        delete_voicemail(mailbox, context)
    if exten and context:
        delete_extension(exten, context)
        delete_lines(exten)

    user = user_helper.find_by_firstname_lastname(firstname, lastname)
    if user:
        delete_lines_for_user(user['id'])
        delete_user(user['id'])


def delete_voicemail(mailbox, context):
    voicemail = voicemail_helper.find_voicemail_by_number(mailbox, context)
    if voicemail:
        voicemail_helper.delete_voicemail(voicemail['id'])


def delete_extension(exten, context):
    extension = extension_helper.find_extension_by_exten_context(exten, context)
    if extension:
        extension_helper.delete_extension(extension['id'])


def delete_lines(exten):
    line_helper.delete_similar_lines(exten)


def delete_lines_for_user(user_id):
    user_lines = user_helper.user_lines_for_user(user_id)
    main = [ul for ul in user_lines if ul['main_user']]
    secondary = [ul for ul in user_lines if not ul['main_user']]
    for user_line in (secondary + main):
        line_helper.delete_line(user_line['line_id'])


def delete_user(user_id):
    user_helper.delete_user(user_id)


def add_or_replace_user(data_dict, step=None):
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

    return user_helper.add_user(data_dict, step=step)


def delete_users_with_profile(profile_name):
    users = world.ws.users.list()
    profiles = [profile for profile in world.ws.cti_profiles.list() if profile.name == profile_name]

    if not profiles:
        raise NoSuchProfileException('The CTI profile %s does not exist.' % profile_name)

    profile_id = profiles[0].id
    for user in users:
        if user.client_profile_id == profile_id:
            if user.voicemail:
                voicemail_helper.delete_voicemail(user.voicemail.id)
            delete_lines_for_user(user.id)
            delete_user(user.id)
