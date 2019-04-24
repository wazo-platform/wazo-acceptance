# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import (
    assert_that,
    is_not,
    none,
)
from lettuce import world
from requests.exceptions import HTTPError

from xivo_acceptance.lettuce import postgres


def add_or_replace_voicemail(parameters):
    delete_similar_voicemails(parameters)
    return create_voicemail(parameters)


def delete_similar_voicemails(parameters):
    number = parameters.get('number')
    if not number:
        return

    context = parameters.get('context', 'default')
    voicemail = find_voicemail_by_number(number, context)
    if not voicemail:
        return

    delete_voicemail(voicemail['id'])


def create_voicemail(parameters):
    return world.confd_client.voicemails.create(parameters)


def delete_voicemail(voicemail_id):
    _delete_associations(voicemail_id)
    _delete_voicemail(voicemail_id)


def _delete_associations(voicemail_id):
    world.confd_client.voicemails(voicemail_id).remove_users()


def _delete_voicemail(voicemail_id):
    world.confd_client.voicemails.delete(voicemail_id)


def find_user_id_for_voicemail(voicemail_id):
    for association in world.confd_client.voicemails(voicemail_id).list_users()['items']:
        return association['user_id']


def find_voicemail_by_user_id(user_id):
    try:
        return world.confd_client.users(user_id).get_voicemail()['voicemail_id']
    except HTTPError:
        return None


def find_voicemail_by_number(number, context='default'):
    voicemails = world.confd_client.voicemails.list(number=number, context=context, recurse=True)['items']
    return voicemails[0] if voicemails else None


def get_voicemail_by_number(number, context='default'):
    voicemail = find_voicemail_by_number(number, context)
    assert_that(
        voicemail,
        is_not(none()),
        "voicemail %s@%s not found" % (number, context)
    )
    return voicemail
