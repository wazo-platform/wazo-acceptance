# -*- coding: utf-8 -*-

# Copyright (C) 2013-2015 Avencall
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

from hamcrest import assert_that, is_not, none


from xivo_acceptance.helpers import dialpattern_helper
from xivo_acceptance.helpers import user_helper
from xivo_acceptance.helpers import group_helper
from xivo_acceptance.helpers import incall_helper
from xivo_acceptance.helpers import meetme_helper
from xivo_acceptance.helpers import queue_helper
from xivo_acceptance.helpers import line_write_helper
from xivo_acceptance.action.confd import extension_action_confd as extension_action
from xivo_acceptance.action.confd import line_extension_action_confd as line_extension_action

from xivo_acceptance.lettuce.postgres import exec_sql_request


def find_extension_by_exten_context(exten, context='default'):
    response = extension_action.all_extensions({'search': exten})
    found = [extension for extension in response.items()
             if extension['exten'] == exten and extension['context'] == context]
    return found[0] if found else None


def find_line_id_for_extension(extension_id):
    response = line_extension_action.get_from_extension(extension_id)
    return response.resource()['line_id'] if response.status_ok() else None


def get_by_exten_context(exten, context='default'):
    extension = find_extension_by_exten_context(exten, context)
    assert_that(extension, is_not(none()),
                "extension %s@%s not found" % (exten, context))
    return extension


def get_by_id(extension_id):
    response = extension_action.get_extension(extension_id)
    return response.resource()


def add_or_replace_extension(extension):
    delete_similar_extensions(extension)
    create_extension(extension)


def create_extension(exteninfo):
    extension = dict(exteninfo)
    if 'id' in extension:
        extension['id'] = int(extension['id'])
    response = extension_action.create_extension(extension)
    return response.resource()


def delete_similar_extensions(extension):
    if 'exten' in extension:
        found_extension = find_extension_by_exten_context(extension['exten'],
                                                          extension.get('context', 'default'))
        if found_extension:
            delete_extension(found_extension['id'])
    if 'id' in extension:
        delete_extension(extension['id'])


def delete_extension(extension_id):
    exten_info = _get_exten_info(extension_id)
    if exten_info:
        _delete_extension_associations(extension_id)
        _delete_extension_type(exten_info['exten'],
                               exten_info['type'],
                               exten_info['typeval'])
        _delete_extension(extension_id)


def _delete_extension_associations(extension_id):
    line_id = find_line_id_for_extension(extension_id)
    if line_id:
        line_write_helper.dissociate_device(line_id)
        line_write_helper.dissociate_extensions(line_id)


def _delete_extension_type(exten, extension_type, typeval):
    if extension_type == 'user':
        user_helper.delete_user(int(typeval))
    elif extension_type == 'queue':
        queue_helper.delete_queues_with_number(exten)
    elif extension_type == 'group':
        group_helper.delete_groups_with_number(exten)
    elif extension_type == 'incall':
        incall_helper.delete_incalls_with_did(exten)
    elif extension_type == 'meetme':
        meetme_helper.delete_meetme_with_confno(exten)
    elif extension_type == 'outcall':
        dialpattern_helper.delete(int(typeval))


def _delete_extension(extension_id):
    # response status isn't checked because a few helpers in
    # _delete_extension_type will implicitly delete the extension and
    # until we get rid of the webi, refactoring them isn't worth it
    extension_action.delete_extension(extension_id)


def _get_exten_info(extension_id):
    query = """
    SELECT
        exten,
        type,
        typeval
    FROM
        extensions
    WHERE
        id = :extension_id
    """
    result = exec_sql_request(query, extension_id=extension_id)
    return result.first()


def get_extension_typeval(extension_id):
    query = "SELECT typeval FROM extensions WHERE id = :extension_id"
    cursor = exec_sql_request(query, extension_id=extension_id)
    return cursor.scalar()
