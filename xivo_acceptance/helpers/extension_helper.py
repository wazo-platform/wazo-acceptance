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

from xivo_lettuce.remote_py_cmd import remote_exec
from xivo_dao.data_handler.extension import services as extension_services
from xivo_lettuce.manager_ws import queue_manager_ws, group_manager_ws, \
    incall_manager_ws, meetme_manager_ws
from xivo_dao.data_handler.exception import ElementDeletionError, \
    ElementNotExistsError
from xivo_acceptance.helpers import dialpattern_helper, user_helper


def find_extension_by_exten(exten):
    return extension_services.find_by_exten(exten)


def get_by_exten_context(exten, context):
    try:
        extension = extension_services.get_by_exten_context(exten, context)
    except ElementNotExistsError:
        return None
    return extension


def delete(extension_id):
    remote_exec(_delete, extension_id=extension_id)


def _delete(channel, extension_id):
    from xivo_dao.data_handler.extension import services as extension_services

    try:
        extension = extension_services.get(extension_id)
    except LookupError:
        return

    extension_services.delete(extension)


def delete_extension_with_exten_context(exten, context):
    remote_exec(_delete_extension_with_exten_context, exten=exten, context=context)


def _delete_extension_with_exten_context(channel, exten, context):
    from xivo_dao.data_handler.extension import services as extension_services

    try:
        extension = extension_services.get_by_exten_context(exten, context)
    except LookupError:
        return

    extension_services.delete(extension)


def delete_all():
    hidden_extensions = extension_services.find_all(commented=True)
    visible_extensions = extension_services.find_all()

    extensions = [e for e in hidden_extensions + visible_extensions if e.context != 'xivo-features']

    for extension in extensions:
        try:
            if extension.type == 'user':
                user_helper.delete_with_user_id(int(extension.typeval))
            elif extension.type == 'queue':
                queue_manager_ws.delete_queues_with_number(extension.exten)
            elif extension.type == 'group':
                group_manager_ws.delete_groups_with_number(extension.exten)
            elif extension.type == 'incall':
                incall_manager_ws.delete_incalls_with_did(extension.exten)
            elif extension.type == 'meetme':
                meetme_manager_ws.delete_meetme_with_confno(extension.exten)
            elif extension.type == 'outcall':
                dialpattern_helper.delete((extension.typeval))

            remote_exec(_delete_all_ule_association_by_extension_id, extension_id=extension.id)

            delete(extension.id)
        except ElementDeletionError:
            pass


def _delete_all_ule_association_by_extension_id(channel, extension_id):
    from xivo_dao.data_handler.user_line_extension import services as ule_services
    from xivo_dao.data_handler.exception import ElementDeletionError

    ules = ule_services.find_all_by_extension_id(extension_id)
    for ule in ules:
        try:
            ule_services.delete_everything(ule)
        except ElementDeletionError:
            pass


def create_extensions(extensions):
    extensions = [dict(e) for e in extensions]
    remote_exec(_create_extensions, extensions=extensions)


def _create_extensions(channel, extensions):
    from xivo_dao.data_handler.extension import services as extension_services
    from xivo_dao.data_handler.extension.model import Extension

    for extinfo in extensions:
        extinfo.setdefault('type', 'user')
        extinfo.setdefault('typeval', '0')
        extension = Extension(**extinfo)
        extension_services.create(extension)
