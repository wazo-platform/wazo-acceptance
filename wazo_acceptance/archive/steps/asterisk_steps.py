# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that
from hamcrest import empty
from hamcrest import has_entries
from hamcrest import has_item
from hamcrest import has_items
from hamcrest import not_
from lettuce import step, world
from xivo_acceptance.helpers import line_read_helper
from xivo_acceptance.lettuce import asterisk, sysutils, common


@step(u'Given the AMI is monitored')
def given_the_ami_is_monitored(step):
    asterisk.start_ami_monitoring()


@step(u'Then I see in the AMI that the line "([^"]*)@(\w+)" has been synchronized')
def then_i_see_in_the_ami_that_the_line_group1_has_been_synchronized(step, extension, context):
    line = line_read_helper.find_with_exten_context(extension, context)
    line_name = line['name']
    lines = [
        'Action: PJSIPNotify',
        'Endpoint: {}'.format(line_name),
        'Variable: Event=check-sync',
    ]

    def _assert():
        ami_lines = asterisk.fetch_ami_lines()
        assert_that(ami_lines, has_items(*lines))

    common.wait_until_assert(_assert, tries=3)


@step('Then I have the following hints')
def then_i_have_the_following_hints(step):
    actual_hints = _list_hints()

    for expected_hint in step.hashes:
        assert_that(actual_hints, has_item(has_entries(expected_hint)))


def _list_hints():
    asterisk_cmd = 'core show hints'
    command = ['asterisk', '-rx', '"{}"'.format(asterisk_cmd)]

    output = sysutils.output_command(command).split('\n')
    output = output[2:-3]  # strip header and footer
    return [_parse_hint(line) for line in output]


def _parse_hint(line):
    hint = {}
    hint['exten'] = line[:20].strip()
    hint['line'] = line[22:44].strip()
    return hint


@step('Then the user "([^"]*)" has the "([^"]*)" hint (enabled|disabled)')
@step('Then the user "([^"]*)" has the "([^"]*)" forward hint (enabled|disabled)')
def then_the_user_has_the_funckey_hint_enabled(step, username, funckey, expected_state):
    firstname, lastname = username.split()
    user = world.confd_client.users.list(firstname=firstname, lastname=lastname)['items'][0]
    prefix_exten = _get_funckey_prefix_exten(user['id'], funckey)
    if expected_state == 'enabled':
        common.wait_until(_assert_inuse_hints_state, prefix_exten, tries=10)
    else:
        common.wait_until(_assert_idle_hints_state, prefix_exten, tries=10)


def _get_funckey_prefix_exten(user_id, funckey):
    funckey_exten = {'unconditional': 21,
                     'noanswer': 22,
                     'busy': 23,
                     'dnd': 25,
                     'incallfilter': 27}
    return '*735{}***2{}'.format(user_id, funckey_exten.get(funckey, ''))


def _get_hints_state(prefix_exten):
    asterisk_cmd = 'core show hint {}'.format(prefix_exten)
    command = ['asterisk', '-rx', '"{}"'.format(asterisk_cmd)]

    output = sysutils.output_command(command).split('\n')
    output = output[:-2]  # strip footer
    return [line[50:66].strip() for line in output]


def _assert_inuse_hints_state(prefix_exten):
    hints_state = _get_hints_state(prefix_exten)
    assert_that(hints_state, not_(empty()))
    for state in hints_state:
        if state != 'InUse':
            return False
    return True


def _assert_idle_hints_state(prefix_exten):
    hints_state = _get_hints_state(prefix_exten)
    assert_that(hints_state, not_(empty()))
    for state in hints_state:
        if state != 'Idle':
            return False
    return True


@step('Then the user "([^"]*)" has all forwards hints disabled')
def then_the_user_has_all_forwards_hints_disabled(step, username):
    firstname, lastname = username.split()
    user = world.confd_client.users.list(firstname=firstname, lastname=lastname)['items'][0]

    forwards = ('unconditional', 'busy', 'noanswer')
    for forward in forwards:
        prefix_exten = _get_funckey_prefix_exten(user['id'], forward)
        common.wait_until(_assert_idle_hints_state, prefix_exten, tries=10)
