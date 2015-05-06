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

from lettuce import world

from xivo_acceptance.helpers import user_helper, group_helper, queue_helper, voicemail_helper
from xivo_acceptance.action.confd import extension_action_confd as extension_action
from xivo_ws import Incall, OverwriteCallerIDMode
from xivo_ws import GroupDestination, QueueDestination, UserDestination, VoicemailDestination


def add_incall(number, context, dst_type, dst_name, caller_id=None):
    incall = Incall()
    incall.number = number
    incall.context = context
    incall.destination = _new_destination(dst_type, dst_name)
    if caller_id:
        incall.caller_id_mode = OverwriteCallerIDMode(caller_id)
    world.ws.incalls.add(incall)


def add_or_replace_incall(number, context, dst_type, dst_name, caller_id=None):
    delete_incalls_with_did(number, context)
    add_incall(number, context, dst_type, dst_name, caller_id)


def _new_destination(dst_type, dst_name):
    dst_type = dst_type.lower()
    if dst_type == 'user':
        return _new_user_destination(dst_name)
    elif dst_type == 'queue':
        return _new_queue_destination(dst_name)
    elif dst_type == 'group':
        return _new_group_destination(dst_name)
    elif dst_type == 'voicemail':
        return _new_voicemail_destination(dst_name)
    else:
        raise Exception('unknown destination type %r' % dst_type)


def _new_user_destination(fullname):
    firstname, lastname = fullname.split()
    user_id = user_helper.get_user_id_with_firstname_lastname(firstname, lastname)
    return UserDestination(user_id)


def _new_queue_destination(queue_name):
    queue_id = queue_helper.find_queue_id_with_name(queue_name)
    return QueueDestination(queue_id)


def _new_group_destination(group_name):
    group_id = group_helper.find_group_id_with_name(group_name)
    return GroupDestination(group_id)


def _new_voicemail_destination(number_context):
    number, _, context = number_context.partition('@')
    voicemail = voicemail_helper.get_voicemail_by_number(number, context)
    return VoicemailDestination(voicemail['id'])


def delete_incalls_with_did(incall_did, context='from-extern'):
    incalls = find_incalls_with_did(incall_did, context)
    for incall in incalls:
        world.ws.incalls.delete(incall.id)
    _delete_extensions_with_did(incall_did, context)


def find_incalls_with_did(incall_did, context='from-extern'):
    return [incall for incall in world.ws.incalls.search_by_number(incall_did)
            if incall.context == context]


def _delete_extensions_with_did(did, context):
    response = extension_action.all_extensions({'search': did})
    extensions = [e for e in response.items()
                  if e['exten'] == did and e['context'] == context]
    for extension in extensions:
        extension_action.delete_extension(extension['id'])
