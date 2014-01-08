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
    _delete_extension(extension_id)


def delete_extension_with_exten_context(exten, context):
    extension = find_extension_by_exten_context(exten, context)
    if extension:
        _delete_extension(extension.id)


def delete_all():
    extension_ids = remote_exec_with_result(_find_all_extension_ids)

    for extension_id in extension_ids:
        _delete_extension(extension_id)


def _delete_extension(extension_id):
    exten_info = remote_exec_with_result(_get_exten_info, extension_id=extension_id)
    if not exten_info:
        return

    exten, extension_type, typeval = exten_info

    remote_exec(_delete_extension_associations, extension_id=extension_id)

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

    remote_exec(_delete_on_server, extension_id=extension_id)


def _delete_on_server(channel, extension_id):
    from xivo_dao.data_handler.extension import services as extension_services

    try:
        extension = extension_services.get(extension_id)
    except LookupError:
        return

    extension_services.delete(extension)


def _find_all_extension_ids(channel):
    from xivo_dao.alchemy.extension import Extension as ExtensionSchema
    from xivo_dao.helpers.db_manager import AsteriskSession

    rows = (AsteriskSession
            .query(ExtensionSchema.id)
            .filter(ExtensionSchema.context != 'xivo-features')
            .all())

    extension_ids = [e.id for e in rows]
    channel.send(extension_ids)


def _get_exten_info(channel, extension_id):
    from xivo_dao.alchemy.extension import Extension as ExtensionSchema
    from xivo_dao.helpers.db_manager import AsteriskSession

    extension_row = (AsteriskSession
                     .query(ExtensionSchema)
                     .filter(ExtensionSchema.id == extension_id)
                     .first())

    if extension_row:
        extension = (extension_row.exten, extension_row.type, extension_row.typeval)
        channel.send(extension)
    else:
        channel.send(None)


def _delete_extension_associations(channel, extension_id):
    from xivo_dao.data_handler.line_extension import dao as line_extension_dao

    line_extension = line_extension_dao.find_by_extension_id(extension_id)
    if line_extension:
        line_extension_dao.dissociate(line_extension)


def create_extensions(extensions):
    extensions = [dict(e) for e in extensions]
    remote_exec(_create_extensions, extensions=extensions)


def _create_extensions(channel, extensions):
    from xivo_dao.data_handler.extension import services as extension_services
    from xivo_dao.data_handler.extension.model import Extension

    for extinfo in extensions:
        extension = Extension(**extinfo)
        extension_services.create(extension)
