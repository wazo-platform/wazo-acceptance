# Copyright 2019-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from behave import then, when
from hamcrest import assert_that, contains_inanyorder, empty, has_entries


@when('a message is left on voicemail "{vm_number}@{vm_context}" by "{cid_name}"')
def when_a_message_is_left_on_voicemail(context, vm_number, vm_context, cid_name):
    context_name = context.helpers.context.get_by(label=vm_context)['name']
    # start the call to the voicemail
    context.helpers.asterisk.send_to_asterisk_cli(
        f'test newid leavevm *97{vm_number} {context_name} 555 {cid_name} SIP'
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
    context_name = context.helpers.context.get_by(label=vm_context)['name']
    # start the call to the voicemail
    context.helpers.asterisk.send_to_asterisk_cli(
        f'test newid checkvm *99{vm_number} {context_name} 555 Test SIP'
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


@when('a message is checked and deleted on voicemail "{vm_number}@{vm_context}"')
def when_a_message_is_checked_and_deleted_on_voicemail(context, vm_number, vm_context):
    context_name = context.helpers.context.get_by(label=vm_context)['name']
    # start the call to the voicemail
    context.helpers.asterisk.send_to_asterisk_cli(
        f'test newid checkvm *99{vm_number} {context_name} 555 Test SIP'
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


@then('there\'s the following messages in voicemail "{vm_number}@{vm_context}"')
def then_there_is_the_following_messages_in_voicemail(context, vm_number, vm_context):
    context_name = context.helpers.context.get_by(label=vm_context)['name']
    vm_conf = context.confd_client.voicemails.list(
        number=vm_number,
        context=context_name,
        recurse=True
    )['items'][0]
    voicemail = context.calld_client.voicemails.get_voicemail(vm_conf['id'])
    messages = _flatten_voicemail_messages(voicemail)
    expected_messages = [has_entries(row.as_dict()) for row in context.table]
    assert_that(messages, contains_inanyorder(*expected_messages))


@then('there\'s no message in voicemail "{vm_number}@{vm_context}"')
def then_there_is_no_message_in_voicemail(context, vm_number, vm_context):
    context_name = context.helpers.context.get_by(label=vm_context)['name']
    vm_conf = context.confd_client.voicemails.list(
        number=vm_number,
        context=context_name,
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
