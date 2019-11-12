# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import random
import string

from behave import given, then
from hamcrest import assert_that, equal_to, is_


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


@given('there are authentication users with info')
def given_there_are_authentication_users_with_info(context):
    for row in context.table:
        body = {
            'firstname': row['firstname'],
            'username': row['username'],
            'password': row['password'],
        }
        context.helpers.user.create(body)


def _check_user_exists(context, username):
    return context.helpers.user.find_by(username=username) is not None


@then('I see a user with username "{username}"')
def then_i_see_a_user_with_username(context, username):
    assert _check_user_exists(context, username)


@then('the user with username "{username}" does not exist')
def then_the_user_with_username_does_not_exist(context, username):
    assert not _check_user_exists(context, username)


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
        context.helpers.user.create(user_body)

        if not body.get('context'):
            # User has no line
            continue

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

        if (body.get('voicemail_name')
                and body.get('voicemail_number')
                and body.get('voicemail_context')):
            voicemail = context.helpers.voicemail.create({
                'name': body['voicemail_name'],
                'context': body['voicemail_context'],
                'number': body['voicemail_number']
            })
            context.helpers.confd_user.add_voicemail(confd_user, voicemail['id'])

        if body.get('agent_number'):
            agent = context.helpers.agent.create({'number': body['agent_number']})
            context.confd_client.users(confd_user).add_agent(agent)

        if endpoint == 'sip' and body.get('with_phone', 'yes') == 'yes':
            tracking_id = "{} {}".format(body['firstname'], body.get('lastname', '')).strip()
            expected_event = {'uuid': confd_user['uuid'], 'line_state': 'available'}
            with context.helpers.bus.wait_for_event('chatd_presence_updated', expected_event):
                _register_and_track_phone(context, tracking_id, sip)


@given('"{firstname} {lastname}" has lines')
def given_the_tlephony_user_has_lines(context, firstname, lastname):
    context.table.require_columns(['name', 'context'])
    confd_user = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)
    for row in context.table:
        body = row.as_dict()

        line = context.helpers.line.create(body)

        endpoint = body.get('endpoint', 'sip')
        if endpoint == 'sip':
            sip = context.helpers.endpoint_sip.create(body)
            context.helpers.line.add_endpoint_sip(line, sip)
        else:
            raise NotImplementedError()

        if body.get('exten') and body['context']:
            extension = context.helpers.extension.find_by(
                exten=body['exten'],
                context=body['context'],
            )
            if not extension:
                extension = context.helpers.extension.create(body)
            context.helpers.line.add_extension(line, extension)

        context.helpers.confd_user.add_line(confd_user, line)

        if endpoint == 'sip' and body.get('with_phone', 'yes') == 'yes':
            _register_and_track_phone(context, body['name'], sip)


def _register_and_track_phone(context, tracking_id, endpoint_sip, nb_phone=1):
    for _ in range(nb_phone):
        phone_config = context.helpers.sip_config.create(endpoint_sip)
        phone = context.helpers.sip_phone.register_line(phone_config)
        phone.sip_contact_uri = context.phone_register.find_new_sip_contact(
            endpoint_sip['username'],
        )
        context.phone_register.add_registered_phone(phone, tracking_id)


@given('"{firstname} {lastname}" has enabled "{dnd_name}" service')
def then_the_user_has_enabled_service(context, firstname, lastname, dnd_name):
    confd_user = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)
    service = {'enabled': True}
    context.confd_client.users(confd_user).update_service(dnd_name, service)


@given('"{firstname} {lastname}" has schedule "{schedule}"')
def given_user_1_has_schedule_2(context, firstname, lastname, schedule):
    confd_user = context.helpers.confd_user.get_by(firtname=firstname, lastname=lastname)
    schedule = context.helpers.schedule.get_by(name=schedule)
    context.confd_client.users(confd_user).add_schedule(schedule['id'])


@given('"{firstname} {lastname}" has reconfigured the line "{exten}@{exten_context}"')
def when_i_reconfigure_the_phone_on_line(context, firstname, lastname, exten, exten_context):
    extension = context.helpers.extension.find_by(
        exten=exten,
        context=exten_context
    )
    line = context.confd_client.lines.get(extension['lines'][0]['id'])
    endpoint_sip = context.confd_client.lines_sip.get(line['endpoint_sip']['id'])
    tracking_id = "{} {}".format(firstname, lastname)
    _register_and_track_phone(context, tracking_id, endpoint_sip)


@given('"{firstname} {lastname}" has an "{forward_name}" forward set to "{exten}"')
def given_user_has_an_unconditional_forward_set_to_exten(context, firstname, lastname, forward_name, exten):
    confd_user = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)
    forward = {'enabled': True, 'destination': exten}
    context.confd_client.users(confd_user).update_forward(forward_name, forward)


@then('"{firstname} {lastname}" has an "{forward_name}" forward set to "{exten}"')
def then_user_has_an_unconditional_forward_set_to_exten(context, firstname, lastname, forward_name, exten):
    confd_user = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)
    forward = context.confd_client.users(confd_user).get_forward(forward_name)
    assert_that(forward['enabled'])
    assert_that(forward['destination'], equal_to(exten))


@then('"{firstname} {lastname}" has no "{forward_name}" forward')
def then_user_has_no_unconditional_forward(context, firstname, lastname, forward_name):
    confd_user = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)
    forward = context.confd_client.users(confd_user).get_forward(forward_name)
    assert_that(forward['enabled'], is_(False))
