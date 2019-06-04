# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import random
import string

from behave import given


def random_string(length, sample=string.ascii_lowercase):
    return ''.join(random.choice(sample) for _ in range(length))


@given('there is an authentication user')
def given_there_is_a_user(context):
    context.username = random_string(10)
    context.password = random_string(10, sample=string.printable)

    body = {
        'firstname': random_string(10),
        'username': context.username,
        'password': context.password,
    }
    context.helpers.user.create(body)


@given('there are telephony users with infos')
def given_there_are_telephony_users_with_infos(context):
    context.table.require_columns(['firstname'])
    for row in context.table:
        body = row.as_dict()

        confd_user = context.helpers.confd_user.create(body)

        user_body = {
            'uuid': confd_user['uuid'],
            'firstname': body['firstname'],
            'lastname': body.get('lastname'),
            'username': body.get('username') or random_string(10),
            'password': body.get('password') or random_string(10, sample=string.printable),
        }
        user = context.helpers.user.create(user_body)

        line = context.helpers.line.create(body)

        endpoint = body.get('endpoint', 'sip')
        if endpoint == 'sip':
            sip = context.helpers.endpoint_sip.create(body)
            context.helpers.line.add_endpoint_sip(line, sip)
        elif endpoint == 'sccp':
            raise NotImplementedError()
        elif endpoint == 'custom':
            raise NotImplementedError()

        if body.get('exten') and body.get('context'):
            extension = context.helpers.extension.create(body)
            context.helpers.line.add_extension(line, extension)

        context.helpers.confd_user.add_line(confd_user, line)

        if body.get('device'):
            device = context.confd_client.devices.list(mac=body['device'])['items'][0]
            context.helpers.line.add_device(line, device)

        # TODO voicemail

        # TODO listen on sip reload event
        import time
        time.sleep(2)

        if endpoint == 'sip' and body.get('with_phone', 'yes') == 'yes':
            _register_and_track_phone(context, user['uuid'], sip)


def _register_and_track_phone(context, user_uuid, endpoint_sip, nb_phone=1):
    for _ in range(nb_phone):
        phone_config = context.helpers.sip_config.create(endpoint_sip)
        phone = context.helpers.sip_phone.register_line(phone_config)
        phone.sip_contact_uri = context.phone_register.find_new_sip_contact(
            endpoint_sip['username'],
        )
        context.phone_register.add_registered_phone(phone, user_uuid)
