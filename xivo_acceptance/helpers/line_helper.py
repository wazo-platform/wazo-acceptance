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

from xivo_lettuce import func
from xivo_lettuce.remote_py_cmd import remote_exec
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
    remote_exec(_delete_all)


def _delete_all(channel):
    from xivo_dao.data_handler.user import services as user_services
    from xivo_dao.data_handler.line import services as line_services
    from xivo_dao.data_handler.extension import services as extension_services
    from xivo_dao.data_handler.user_line_extension import dao as ule_dao
    from xivo_dao.data_handler.exception import ElementDeletionError
    from xivo_dao.data_handler.exception import ElementNotExistsError

    for line in line_services.find_all():

        links = ule_dao.find_all_by_line_id(line.id)
        for link in links:
            try:
                ule_dao.delete(link)
            except (ElementDeletionError, ElementNotExistsError):
                pass

            try:
                user = user_services.get(link.user_id)
                user_services.delete(user)
            except (ElementDeletionError, ElementNotExistsError):
                pass

            if link.extension_id:
                try:
                    extension = extension_services.get(link.extension_id)
                    extension_services.delete(extension)
                except (ElementDeletionError, ElementNotExistsError):
                    pass

        try:
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
