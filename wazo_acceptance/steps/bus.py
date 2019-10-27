# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import collections
import queue

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
    event = context.helpers.bus.pop_received_event()
    assert_that(event, has_entries(name=event_name))
    assert_that(event, has_key('data'))
    result = _flatten_nested_dict(event['data'])
    assert_that(result, has_entries(context.table[0].as_dict()))


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
