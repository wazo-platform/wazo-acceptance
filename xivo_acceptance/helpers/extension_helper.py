# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import world

from requests.exceptions import HTTPError

from xivo_acceptance.helpers import dialpattern_helper
from xivo_acceptance.helpers import entity_helper
from xivo_acceptance.helpers import user_helper
from xivo_acceptance.helpers import group_helper
from xivo_acceptance.helpers import incall_helper
from xivo_acceptance.helpers import queue_helper
from xivo_acceptance.helpers import line_write_helper

from xivo_acceptance.lettuce.postgres import exec_sql_request


def find_extension_by_exten_context(exten, context='default'):
    try:
        return get_by_exten_context(exten, context)
    except IndexError:
        return None


def get_by_exten_context(exten, context='default'):
    entity = entity_helper.get_default_entity()
    return world.confd_client.extensions.list(
        exten=exten,
        context=context,
        tenant_uuid=entity['tenant']['uuid'],
        recurse=True,
    )['items'][0]


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
        _delete_meetme(exten)
    elif extension_type == 'outcall':
        dialpattern_helper.delete(int(typeval))


def _delete_meetme(exten):
    raise NotImplementedError


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
