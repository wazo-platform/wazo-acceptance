# -*- coding: utf-8 -*-
# Copyright (C) 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

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
    elif type_ == 'ivr':
        key_id = _build_ivr_destination(args)
    else:
        key_id = args

    result = {'type': type_}
    result.update(key_id)
    return result


def _build_user_destination(fullname):
    firstname, lastname = fullname.split()
    user = user_helper.get_by_firstname_lastname(firstname, lastname)
    return {'user_id': user['id']}


def _build_queue_destination(queue_name):
    queue_id = queue_helper.get_queue_by(name=queue_name)['id']
    return {'queue_id': queue_id}


def _build_group_destination(group_name):
    group = group_helper.get_group_by_name(group_name)
    return {'group_id': group['id']}


def _build_voicemail_destination(number_context):
    number, _, context = number_context.partition('@')
    voicemail = voicemail_helper.get_voicemail_by_number(number, context)
    return {'voicemail_id': voicemail['id']}


def _build_ivr_destination(ivr_name):
    ivr_id = world.confd_client.ivr.list(name=ivr_name)['items'][0]['id']
    return {'ivr_id': ivr_id}


def delete_incalls_with_did(incall_did, context='from-extern'):
    extensions = world.confd_client.extensions.list(exten=incall_did, context=context, recurse=True)
    for extension in extensions['items']:
        if extension['incall']:
            world.confd_client.incalls.delete(extension['incall']['id'])
        world.confd_client.extensions.delete(extension['id'])
