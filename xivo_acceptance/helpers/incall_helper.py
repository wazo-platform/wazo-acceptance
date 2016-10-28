# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
# Copyright (C) 2016 Proformatique Inc.
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

from xivo_acceptance.helpers import user_helper, group_helper, queue_helper, voicemail_helper


def add_or_replace_incall(exten, context, dst_type, dst_name, caller_id=None):
    delete_incalls_with_did(exten, context)
    add_incall(exten, context, dst_type, dst_name, caller_id)


def add_incall(exten, context, dst_type, dst_name, caller_id=None):
    destination = _build_destination(dst_type, dst_name)
    incall = {'destination': destination,
              'caller_id_mode': 'overwrite',
              'caller_id_name': caller_id}
    extension = {'exten': exten,
                 'context': context}

    incall = world.confd_client.incalls.create(incall)
    extension = world.confd_client.extensions.create(extension)
    world.confd_client.incalls(incall['id']).add_extension(extension)


def _build_destination(type_, args):
    type_ = type_.lower()
    key_id = {}
    if type_ == 'user':
        key_id = _build_user_destination(args)
    elif type_ == 'queue':
        key_id = _build_queue_destination(args)
    elif type_ == 'group':
        key_id = _build_group_destination(args)
    elif type_ == 'voicemail':
        key_id = _build_voicemail_destination(args)

    result = {'type': type_}
    result.update(key_id)
    return result


def _build_user_destination(fullname):
    firstname, lastname = fullname.split()
    user = user_helper.get_by_firstname_lastname(firstname, lastname)
    return {'user_id': user['id']}


def _build_queue_destination(queue_name):
    queue_id = queue_helper.find_queue_id_with_name(queue_name)
    return {'queue_id': queue_id}


def _build_group_destination(group_name):
    group_id = group_helper.find_group_id_with_name(group_name)
    return {'group_id': group_id}


def _build_voicemail_destination(number_context):
    number, _, context = number_context.partition('@')
    voicemail = voicemail_helper.get_voicemail_by_number(number, context)
    return {'voicemail_id': voicemail['id']}


def delete_incalls_with_did(incall_did, context='from-extern'):
    extensions = world.confd_client.extensions.list(exten=incall_did, context=context)
    for extension in extensions['items']:
        if extension['incall']:
            world.confd_client.incalls.delete(extension['incall']['id'])
        world.confd_client.extensions.delete(extension['id'])
