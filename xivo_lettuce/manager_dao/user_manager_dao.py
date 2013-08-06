# -*- coding: utf-8 -*-
#
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

from execnet.gateway_base import RemoteError
from xivo_lettuce.remote_py_cmd import remote_exec
from xivo_dao.data_handler.user import services as user_services
from xivo_dao.data_handler.exception import ElementNotExistsError
from xivo_lettuce.manager_dao import voicemail_manager_dao


def delete_user_line_extension_voicemail(firstname, lastname, context=None, exten=None, mailbox=None):
    if exten and context:
        delete_user_line_extension_with_exten_context(exten, context)
    if mailbox and context:
        voicemail_manager_dao.delete_voicemail_with_number_context(mailbox, context)
    delete_user_line_extension_with_firstname_lastname(firstname, lastname)
    delete_all_user_with_firstname_lastname(firstname, lastname)


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


def is_user_with_name_exists(firstname, lastname):
    user = user_services.find_by_firstname_lastname(firstname, lastname)
    if user is None:
        return False
    return True


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
    from xivo_dao.data_handler.user_line_extension import services as ule_services

    ules = ule_services.find_all_by_user_id(user_id)

    if ules:
        for ule in ules:
            ule_services.delete_everything(ule)


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
