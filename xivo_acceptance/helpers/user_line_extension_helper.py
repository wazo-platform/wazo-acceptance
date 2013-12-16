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
from xivo_lettuce.exception import NoSuchProfileException


def delete_user_line_extension_voicemail(firstname, lastname, context=None, exten=None, mailbox=None):
    if exten and context:
        extension_helper.delete_extension_with_exten_context(exten, context)
    if mailbox and context:
        voicemail_helper.delete_voicemail_with_number_context(mailbox, context)
    delete_user_line_extension_with_firstname_lastname(firstname, lastname)
    user_helper.delete_all_user_with_firstname_lastname(firstname, lastname)


def delete_user_line_extension_with_firstname_lastname(firstname, lastname):
    user = user_helper.find_by_firstname_lastname(firstname, lastname)
    if user:
        delete_user_line_extension_with_user_id(user.id)


def delete_user_line_extension_with_user_id(user_id):
    user = user_helper.get_by_user_id(user_id)
    if not user:
        return

    line_id = user_helper.find_line_id_for_user(user_id)
    if line_id:
        line_helper.delete_line(line_id)

    extension_id = extension_helper.find_extension_id_for_line(line_id)
    if extension_id:
        extension_helper.delete(extension_id)

    user_helper.delete_user(user.id)


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

    return user_helper.add_user(data_dict)


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
