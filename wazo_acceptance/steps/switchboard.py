# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given, then, when


@given('there are switchboards with infos')
def given_there_are_switchboards_with_infos(context):
    context.table.require_columns(['name'])
    for row in context.table:
        body = row.as_dict()
        timeout = body.pop('timeout', None)
        if timeout:
            body['timeout'] = int(timeout)
        switchboard = context.helpers.switchboard.create(body)
        members = body['members'].split(',') if body.get('members') else []
        users = [context.helpers.confd_user.get_by(fullname=name) for name in members]
        context.confd_client.switchboards(switchboard).update_user_members(users)

        if body.get('noanswer_destination'):
            type_, name = body['noanswer_destination'].split(':')
            fallbacks_body = {'noanswer_destination': {'type': type_}}
            if type_ == 'hangup':
                fallbacks_body['noanswer_destination']['cause'] = 'normal'
            else:
                raise NotImplementedError('Destination not implemented: {}'.format(type_))
            context.confd_client.switchboards(switchboard).update_fallbacks(fallbacks_body)


@then('switchboard "{name}" has "{caller_name}" in queued calls')
def then_switchboard_has_callerid_in_queued_calls(context, name, caller_name):
    switchboard = context.helpers.switchboard.get_by(name=name)
    calls = context.calld_client.switchboards.list_queued_calls(switchboard['uuid'])
    caller_numbers = [call['caller_id_number'] for call in calls['items']]
    caller_names = [call['caller_id_name'] for call in calls['items']]
    assert caller_name in (caller_names + caller_numbers)


@then('switchboard "{name}" has "{caller_name}" in held calls')
def then_switchboard_has_callerid_in_held_calls(context, name, caller_name):
    switchboard = context.helpers.switchboard.get_by(name=name)
    calls = context.calld_client.switchboards.list_held_calls(switchboard['uuid'])
    caller_numbers = [call['caller_id_number'] for call in calls['items']]
    caller_names = [call['caller_id_name'] for call in calls['items']]
    assert caller_name in (caller_names + caller_numbers)


@when('"{firstname} {lastname}" answer queued call "{caller_name}" from switchboard "{name}"')
def when_user_answer_queued_call_from_switchboard(context, firstname, lastname, caller_name, name):
    switchboard = context.helpers.switchboard.get_by(name=name)
    call = context.helpers.switchboard.get_queued_call_by(
        switchboard['uuid'],
        caller_id_number=caller_name,
    )

    tracking_id = "{} {}".format(firstname, lastname)
    token = context.helpers.token.get(tracking_id)['token']
    with context.helpers.utils.set_token(context.calld_client, token):
        context.calld_client.switchboards.answer_queued_call_from_user(
            switchboard['uuid'],
            call['id'],
        )


@when('"{firstname} {lastname}" answer held call "{caller_name}" from switchboard "{name}"')
def when_user_answer_held_call_from_switchboard(context, firstname, lastname, caller_name, name):
    switchboard = context.helpers.switchboard.get_by(name=name)
    call = context.helpers.switchboard.get_held_call_by(
        switchboard['uuid'],
        caller_id_number=caller_name,
    )
    tracking_id = "{} {}".format(firstname, lastname)
    token = context.helpers.token.get(tracking_id)['token']
    with context.helpers.utils.set_token(context.calld_client, token):
        context.calld_client.switchboards.answer_held_call_from_user(
            switchboard['uuid'],
            call['id']
        )


@when('"{firstname} {lastname}" put call "{caller_name}" from switchboard "{name}" on hold')
def when_user_put_call_from_switchboard_on_hold(context, firstname, lastname, caller_name, name):
    switchboard = context.helpers.switchboard.get_by(name=name)
    call = context.helpers.call.get_by(user_uuid=None, caller_id_number=caller_name)
    context.calld_client.switchboards.hold_call(switchboard['uuid'], call['call_id'])
