# Copyright 2020-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from behave import given, when
from datetime import datetime, timedelta

from wazo_test_helpers import until


@given('there are no hour change in the next {seconds} seconds')
def given_no_hour_change_in_next_1_seconds(context, seconds):
    seconds = int(seconds)
    now = datetime.now()
    delta_until_next_hour = timedelta(hours=1) - timedelta(minutes=now.minute, seconds=now.second)
    if delta_until_next_hour.total_seconds() < seconds:
        time.sleep(seconds)


@when('I wait until call with caller ID name "{cid_name}" to be over')
def step_impl(context, cid_name):
    def call_is_up():
        calls = context.calld_client.calls.list_calls()
        for call in calls['items']:
            if call['caller_id_name'] == cid_name:
                return True
        return False

    until.false(
        call_is_up,
        timeout=30,
        message=f'call with caller ID name "{cid_name}" never finished',
    )


@when('I wait {seconds} seconds during my pause')
@when('I wait {seconds} seconds for the call hangs up for everyone')
@when('I wait {seconds} seconds for the call processing with slow machine')
@when('I wait {seconds} seconds for the call processing')
@when('I wait {seconds} seconds for the call to be forwarded')
@when('I wait {seconds} seconds for the end of ringing time')
@when('I wait {seconds} seconds for the password input message to complete')
@when('I wait {seconds} seconds for the no permission message to complete')
@when('I wait {seconds} seconds for the timeout to expire')
@when('I wait {seconds} seconds for the timeout to not expire')
@when('I wait {seconds} seconds for the transfer lock release')
@when('I wait {seconds} seconds for wazo-calld load to drop')
@when('I wait {seconds} seconds to play unreachable message')
@when('I wait {seconds} seconds to play message')
@when('I wait {seconds} seconds to simulate call center')
@when('I wait {seconds} seconds until the wrapup completes')
@when('I wait {seconds} seconds while being logged on')
@when('I wait {seconds} seconds')
def when_i_wait_n_seconds(context, seconds):
    _sleep(seconds)


def _sleep(seconds):
    time.sleep(float(seconds))
