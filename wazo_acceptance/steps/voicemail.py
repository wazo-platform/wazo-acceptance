# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from hamcrest import (
    assert_that,
    contains_inanyorder,
    empty,
    has_entries,
    has_key,
)
from behave import (
    given,
    then,
    when,
)


@when('a message is left on voicemail "{mailbox}" by "{cid_name}"')
def when_a_message_is_left_on_voicemail(context, mailbox, cid_name):
    vm_number, vm_context = mailbox.split(u'@', 1)
    # start the call to the voicemail
    context.helpers.asterisk.send_to_asterisk_cli(
        'test newid leavevm *97{} {} 555 {} SIP'.format(vm_number, vm_context, cid_name)
    )
    # press '#' to leave a message right away
    time.sleep(2)
    context.helpers.asterisk.send_to_asterisk_cli(
        'test dtmf SIP/auto-leavevm #'
    )
    # hangup after leaving a small message
    time.sleep(2)
    context.helpers.asterisk.send_to_asterisk_cli(
        'channel request hangup SIP/auto-leavevm'
    )


@when('a message is checked and kept on voicemail "{vm_number}@{vm_context}"')
def when_a_message_is_checked_and_kept_on_voicemail(context, vm_number, vm_context):
    # start the call to the voicemail
    context.helpers.asterisk.send_to_asterisk_cli(
        'test newid checkvm *99{} {} 555 Test SIP'.format(vm_number, vm_context)
    )
    # press '1' to listen to first message
    time.sleep(2)
    context.helpers.asterisk.send_to_asterisk_cli(
        'test dtmf SIP/auto-checkvm 1'
    )
    # press '1' to skip announce
    time.sleep(1)
    context.helpers.asterisk.send_to_asterisk_cli(
        'test dtmf SIP/auto-checkvm 1'
    )
    # hangup after hearing the message
    time.sleep(2)
    context.helpers.asterisk.send_to_asterisk_cli(
        'channel request hangup SIP/auto-checkvm'
    )


@when('a message is checked and deleted on voicemail "{mailbox}"')
def when_a_message_is_checked_and_deleted_on_voicemail(context, mailbox):
    vm_number, vm_context = mailbox.split(u'@', 1)
    # start the call to the voicemail
    context.helpers.asterisk.send_to_asterisk_cli(
        'test newid checkvm *99{} {} 555 Test SIP'.format(vm_number, vm_context)
    )
    # press '1' to listen to first message
    time.sleep(2)
    context.helpers.asterisk.send_to_asterisk_cli(
        'test dtmf SIP/auto-checkvm 1'
    )
    # press '1' to skip announce
    time.sleep(1)
    context.helpers.asterisk.send_to_asterisk_cli(
        'test dtmf SIP/auto-checkvm 1'
    )
    # press '7' to delete the message
    time.sleep(1)
    context.helpers.asterisk.send_to_asterisk_cli(
        'test dtmf SIP/auto-checkvm 7'
    )
    # hangup
    time.sleep(1)
    context.helpers.asterisk.send_to_asterisk_cli(
        'channel request hangup SIP/auto-checkvm'
    )


@given('I listen on the bus for "{event_name}" messages')
def given_i_listen_on_the_bus_for_messages(context, event_name):
    context.helpers.bus.subscribe([event_name])


@then('I receive a voicemail message event "{event_name}" with data')
def then_i_receive_a_voicemail_message_event_on_queue(context, event_name):
    event = context.helpers.bus.pop_received_event()
    assert_that(event, has_entries({'name': event_name, 'data': has_key('message')}))
    message = _flatten_message(event['data']['message'])
    assert_that(message, has_entries(context.table[0].as_dict()))


@then('there\'s the following messages in voicemail "{vm_number}@{vm_context}"')
def then_there_is_the_following_messages_in_voicemail(context, vm_number, vm_context):
    vm_conf = context.confd_client.voicemails.list(
        number=vm_number,
        context=vm_context,
        recurse=True
    )['items'][0]
    voicemail = context.calld_client.voicemails.get_voicemail(vm_conf['id'])
    messages = _flatten_voicemail_messages(voicemail)
    expected_messages = [has_entries(row.as_dict()) for row in context.table]
    assert_that(messages, contains_inanyorder(*expected_messages))


@then('there\'s no message in voicemail "{vm_number}@{vm_context}"')
def then_there_is_no_message_in_voicemail(context, vm_number, vm_context):
    vm_conf = context.confd_client.voicemails.list(
        number=vm_number,
        context=vm_context,
        recurse=True
    )['items'][0]
    voicemail = context.calld_client.voicemails.get_voicemail(vm_conf['id'])
    messages = _flatten_voicemail_messages(voicemail)
    assert_that(messages, empty())


def _flatten_voicemail_messages(voicemail):
    flat_messages = []
    for folder in voicemail['folders']:
        for message in folder['messages']:
            flat_message = dict(message)
            flat_message['folder_type'] = folder['type']
            flat_message['folder_name'] = folder['name']
            flat_message['folder_id'] = folder['id']
            flat_messages.append(flat_message)
    return flat_messages


def _flatten_message(message):
    flat_message = dict(message)
    folder = flat_message.pop('folder')
    flat_message['folder_type'] = folder['type']
    flat_message['folder_name'] = folder['name']
    flat_message['folder_id'] = folder['id']
    return flat_message


def _extract_voicemail_info_to_confd(row):
    voicemail = dict(row)

    if 'max_messages' in voicemail and voicemail['max_messages'] is not None and voicemail['max_messages'].isdigit():
        voicemail['max_messages'] = int(voicemail['max_messages'])

    for key in ['attach_audio', 'delete_messages', 'ask_password']:
        if key in voicemail:
            voicemail[key] = (voicemail[key] == 'true')

    return voicemail
