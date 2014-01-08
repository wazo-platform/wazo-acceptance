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

from xivo_lettuce import func
from xivo_lettuce.remote_py_cmd import remote_exec, remote_exec_with_result
from xivo_dao.data_handler.exception import ElementNotExistsError
from xivo_dao.data_handler.line import services as line_services


def is_with_exten_context_exists(exten, context):
    try:
        find_with_exten_context(exten, context)
    except Exception:
        return False
    return True


def find_with_exten_context(exten, context):
    try:
        line = line_services.get_by_number_context(exten, context)
    except ElementNotExistsError:
        raise Exception('expecting line with number %r and context %r not found' % (exten, context))
    return line


def find_with_extension(extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    return find_with_exten_context(number, context)


def find_with_name(name):
    return line_services.find_all_by_name(name)


def find_with_user_id(user_id):
    try:
        line = line_services.get_by_user_id(user_id)
    except ElementNotExistsError:
        raise Exception('expecting line with user ID %r not found' % (user_id))
    return line


def find_line_id_with_exten_context(exten, context):
    line = find_with_exten_context(exten, context)
    return line.id


def delete_line_with_exten_context(exten, context):
    remote_exec(_delete_line_with_exten_context, exten=exten, context=context)


def _delete_line_with_exten_context(channel, exten, context):
    from xivo_dao.data_handler.line import services as line_services

    try:
        line = line_services.get_by_number_context(exten, context)
    except LookupError:
        return

    line_services.delete(line)


def delete_all():
    line_ids = remote_exec_with_result(_all_line_ids)
    for line_id in line_ids:
        remote_exec(_delete_line, line_id=line_id)


def _all_line_ids(channel):
    from xivo_dao.data_handler.line import services as line_services
    lines = line_services.find_all()
    line_ids = [line.id for line in lines]
    channel.send(line_ids)


def delete_line(line_id):
    remote_exec(_delete_line, line_id=line_id)


def _delete_line(channel, line_id):
    from xivo_dao.data_handler.exception import ElementDeletionError
    from xivo_dao.data_handler.exception import ElementNotExistsError
    from xivo_dao.data_handler.line import services as line_services
    from xivo_dao.data_handler.line_extension import dao as line_extension_dao
    from xivo_dao.data_handler.user_line import dao as user_line_dao

    user_lines = user_line_dao.find_all_by_line_id(line_id)
    for user_line in user_lines:
        user_line_dao.dissociate(user_line)

    line_extension = line_extension_dao.find_by_line_id(line_id)
    if line_extension:
        line_extension_dao.dissociate(line_extension)

    try:
        line = line_services.get(line_id)
        line_services.delete(line)
    except (ElementDeletionError, ElementNotExistsError):
        pass


def create(parameters):
    remote_exec(_create, parameters=parameters)


def _create(channel, parameters):
    from xivo_dao.data_handler.line import services as line_services
    from xivo_dao.data_handler.line.model import Line

    line = Line(**parameters)
    line_services.create(line)
