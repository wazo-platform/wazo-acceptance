# Copyright 2019-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import then

from hamcrest import (
    assert_that,
    empty,
    has_entries,
    has_item,
    not_,
)
from xivo_test_helpers import until

FORWARDS = ('unconditional', 'busy', 'noanswer')
FUNCKEYS_EXTEN = {
    'unconditional': 21,
    'noanswer': 22,
    'busy': 23,
    'enablednd': 25,
    'incallfilter': 27,
}


@then('I have the following hints')
def then_i_have_the_following_hints(context):
    output = context.helpers.asterisk.send_to_asterisk_cli('core show hints').split('\n')
    output = output[2:-3]  # strip header and footer
    hints = [{'exten': line[:20].strip(), 'line': line[22:44].strip()} for line in output]

    for row in context.table:
        row = row.as_dict()
        assert_that(hints, has_item(has_entries(row)))


@then('"{firstname} {lastname}" has function key "{position}" hint enabled')
def then_the_user_has_funckey_hint_enabled(context, firstname, lastname, position):
    confd_user = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)
    funckey = context.confd_client.users(confd_user).get_funckey(int(position))
    prefix_exten = _get_funckey_prefix_exten(confd_user['id'], funckey)
    until.true(_assert_inuse_hints_state, context, prefix_exten, tries=10)


@then('"{firstname} {lastname}" has function key "{position}" hint disabled')
def then_the_user_has_funckey_hint_disabled(context, firstname, lastname, position):
    confd_user = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)
    funckey = context.confd_client.users(confd_user).get_funckey(int(position))
    prefix_exten = _get_funckey_prefix_exten(confd_user['id'], funckey)
    until.true(_assert_idle_hints_state, context, prefix_exten, tries=10)


def _get_funckey_prefix_exten(user_id, funckey):
    if funckey['destination']['type'] == 'forward':
        funckey_exten = FUNCKEYS_EXTEN[funckey['destination']['forward']]
        if funckey['destination']['exten']:
            funckey_exten = '{}*{}'.format(funckey_exten, funckey['destination']['exten'])
    elif funckey['destination']['type'] == 'service':
        funckey_exten = FUNCKEYS_EXTEN[funckey['destination']['service']]
    else:
        raise Exception('Function key exten not found')

    return '*735{}***2{}'.format(user_id, funckey_exten)


def _assert_inuse_hints_state(context, prefix_exten):
    hints_state = _get_hints_state(context, prefix_exten)
    assert_that(hints_state, not_(empty()))
    for state in hints_state:
        if state != 'InUse':
            return False
    return True


def _assert_idle_hints_state(context, prefix_exten):
    hints_state = _get_hints_state(context, prefix_exten)
    assert_that(hints_state, not_(empty()))
    for state in hints_state:
        if state != 'Idle':
            return False
    return True


def _get_hints_state(context, prefix_exten):
    asterisk_cmd = 'core show hint {}'.format(prefix_exten)
    command = ['asterisk', '-rx', '"{}"'.format(asterisk_cmd)]

    output = context.remote_sysutils.output_command(command).split('\n')
    output = output[:-2]  # strip footer
    return [line[50:66].strip() for line in output]


@then('"{firstname} {lastname}" has all forwards hints enabled')
def then_the_user_has_all_forwards_hints_enabled(context, firstname, lastname):
    confd_user = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)
    for forward in FORWARDS:
        funckey = {'destination': {'type': 'forward', 'forward': forward, 'exten': None}}
        prefix_exten = _get_funckey_prefix_exten(confd_user['id'], funckey)
        until.true(_assert_inuse_hints_state, context, prefix_exten, tries=10)


@then('"{firstname} {lastname}" has all forwards hints disabled')
def then_the_user_has_all_forwards_hints_disabled(context, firstname, lastname):
    confd_user = context.helpers.confd_user.get_by(firstname=firstname, lastname=lastname)
    for forward in FORWARDS:
        funckey = {'destination': {'type': 'forward', 'forward': forward, 'exten': None}}
        prefix_exten = _get_funckey_prefix_exten(confd_user['id'], funckey)
        until.true(_assert_idle_hints_state, context, prefix_exten, tries=10)
