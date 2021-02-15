# Copyright 2019-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import collections
import queue
import time

from behave import (
    given,
    then,
)
from hamcrest import (
    assert_that,
    empty,
    has_entries,
    has_key,
)

from xivo_test_helpers import until


@given('I listen on the bus for "{event_name}" messages')
def given_i_listen_on_the_bus_for_messages(context, event_name):
    context.helpers.bus.subscribe([event_name])


@then('I receive no "{event_name}" event')
def then_i_receive_no_event_on_queue(context, event_name):
    try:
        events = context.helpers.bus.pop_received_event(timeout=3)
        assert_that(events, empty())
    except queue.Empty:
        pass


@then('I receive a "{event_name}" event')
def then_i_receive_a_message(context, event_name):
    events = context.helpers.bus.pop_received_event()
    assert_that(events, has_entries(name=event_name))


@then('I receive a "{event_name}" event with data')
def then_i_receive_a_event_on_queue(context, event_name):
    def event_match():
        event = context.helpers.bus.pop_received_event()
        assert_that(event, has_entries(name=event_name))
        assert_that(event, has_key('data'))
        result = _flatten_nested_dict(event['data'])
        assert_that(result, has_entries(context.table[0].as_dict()))

    until.assert_(event_match, interval=0.1, tries=10)

    # NOTE(fblackburn): When an event is triggered, the database is not committed. Sometime, a
    # race condition can occur (mostly on single core host) between the event sent and the
    # database commit. Adding delay help to avoid this race condition.
    time.sleep(0.1)


@then('I receive a "{event_name}" event with "{wrapper}" data')
def then_i_receive_a_event_with_wrapper_on_queue(context, event_name, wrapper):
    event = context.helpers.bus.pop_received_event()
    assert_that(event, has_entries(name=event_name, data=has_key(wrapper)))
    result = _flatten_nested_dict(event['data'][wrapper])
    assert_that(result, has_entries(context.table[0].as_dict()))


def _flatten_nested_dict(dict_, parent_key='', separator='_'):
    items = []
    for key, value in dict_.items():
        new_key = '{parent_key}{separator}{key}'.format(
            parent_key=parent_key, separator=separator, key=key
        ) if parent_key else key
        if isinstance(value, collections.MutableMapping):
            items.extend(_flatten_nested_dict(value, new_key, separator=separator).items())
        else:
            items.append((new_key, value))
    return dict(items)


@then('I see in the AMI that the line "{exten}@{exten_context}" has been synchronized')
def then_i_receive_an_ami_event_that_the_line_has_been_synchronized(context, exten, exten_context):
    extension = context.helpers.extension.get_by(exten=exten, context=exten_context)
    line_name = extension['lines'][0]['name']
    path = 'rawman'
    action = 'action=PJSIPNotify'
    variable = 'Variable=Event%3Dcheck-sync'
    endpoint = f'Endpoint={line_name}'
    expected = f'{path}?{action}\\&{variable}\\&{endpoint} HTTP/1.1\\" 200'
    # NOTE(fblackburn): can be improved by scoping the log with timestamp
    command = ['grep', '-q', expected, '/var/log/wazo-amid.log']

    until.assert_(context.ssh_client.check_call, command, tries=3)
