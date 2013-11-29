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

from xivo_acceptance.helpers import dialpattern_helper, user_helper, \
    group_helper, incall_helper, meetme_helper, queue_helper
from xivo_dao.data_handler.extension import services as extension_services
from xivo_dao.data_handler.exception import ElementDeletionError, \
    ElementNotExistsError
from xivo_lettuce.remote_py_cmd import remote_exec, remote_exec_with_result


def find_extension_by_exten(exten):
    return extension_services.find_by_exten(exten)


def find_extension_by_exten_context(exten, context):
    return extension_services.find_by_exten_context(exten, context)


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
    all_extensions = remote_exec_with_result(_find_all_extensions)

    for extension in all_extensions:
        extension_id, exten, extension_type, typeval = extension

        remote_exec(_delete_all_ule_association_by_extension_id, extension_id=extension_id)

        try:
            if extension_type == 'user':
                user_helper.delete_with_user_id(int(typeval))
            elif extension_type == 'queue':
                queue_helper.delete_queues_with_number(exten)
            elif extension_type == 'group':
                group_helper.delete_groups_with_number(exten)
            elif extension_type == 'incall':
                incall_helper.delete_incalls_with_did(exten)
            elif extension_type == 'meetme':
                meetme_helper.delete_meetme_with_confno(exten)
            elif extension_type == 'outcall':
                dialpattern_helper.delete((typeval))
        except ElementDeletionError as e:
            print "I tried deleting a type %s typeval %s but it didn't work." % (extension_type, typeval)
            print e

        delete(extension_id)


def _find_all_extensions(channel):
    from xivo_dao.alchemy.extension import Extension as ExtensionSchema
    from xivo_dao.helpers.db_manager import AsteriskSession

    extension_rows = (AsteriskSession
                      .query(ExtensionSchema)
                      .filter(ExtensionSchema.context != 'xivo-features')
                      .all())

    extensions = [(e.id, e.exten, e.type, e.typeval) for e in extension_rows]
    channel.send(extensions)


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
        extension = Extension(**extinfo)
        extension_services.create(extension)
