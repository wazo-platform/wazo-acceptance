# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import queue

from behave import (
    given,
    then,
)

from hamcrest import (
    assert_that,
    empty,
    has_entries,
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
