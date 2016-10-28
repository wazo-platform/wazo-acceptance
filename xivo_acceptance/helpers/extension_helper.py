# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
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

from requests.exceptions import HTTPError

from xivo_acceptance.helpers import dialpattern_helper
from xivo_acceptance.helpers import user_helper
from xivo_acceptance.helpers import group_helper
from xivo_acceptance.helpers import incall_helper
from xivo_acceptance.helpers import meetme_helper
from xivo_acceptance.helpers import queue_helper
from xivo_acceptance.helpers import line_write_helper

from xivo_acceptance.lettuce.postgres import exec_sql_request


def find_extension_by_exten_context(exten, context='default'):
    try:
        return get_by_exten_context(exten, context)
    except IndexError:
        return None


def find_by_id(extension_id):
    try:
        return get_by_id(extension_id)
    except HTTPError:
        return None


def get_by_exten_context(exten, context='default'):
    return world.confd_client.extensions.list(exten=exten, context=context)['items'][0]


def get_by_id(extension_id):
    return world.confd_client.extensions.get(extension_id)


def add_or_replace_extension(extension):
    delete_similar_extensions(extension)
    create_extension(extension)


def create_extension(exteninfo):
    return world.confd_client.extensions.create(exteninfo)


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
    lines = get_by_id(extension_id)['lines']
    for line in lines:
        line = world.confd_client.lines.get(line['id'])
        line_write_helper.dissociate_device(line)
        line_write_helper.dissociate_extensions(line)


def _delete_extension_type(exten, extension_type, typeval):
    if extension_type == 'user' and typeval != '0':
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
    try:
        world.confd_client.extensions.delete(extension_id)
    except HTTPError:
        pass


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
