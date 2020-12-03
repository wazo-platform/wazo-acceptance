# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from behave import given, when
from datetime import datetime, timedelta


@given('there are no hour change in the next {seconds} seconds')
def given_no_hour_change_in_next_1_seconds(context, seconds):
    seconds = int(seconds)
    now = datetime.now()
    delta_until_next_hour = timedelta(hours=1) - timedelta(minutes=now.minute, seconds=now.second)
    if delta_until_next_hour.total_seconds() < seconds:
        time.sleep(seconds)


@when('I wait {seconds} seconds during my pause')
@when('I wait {seconds} seconds for the call processing with slow machine')
@when('I wait {seconds} seconds for the call processing')
@when('I wait {seconds} seconds for the call to be forwarded')
@when('I wait {seconds} seconds for the end of ringing time')
@when('I wait {seconds} seconds for the no permission message to complete')
@when('I wait {seconds} seconds for the timeout to expire')
@when('I wait {seconds} seconds for the timeout to not expire')
@when('I wait {seconds} seconds for wazo-calld load to drop')
@when('I wait {seconds} seconds to play unreachable message')
@when('I wait {seconds} seconds to simulate call center')
@when('I wait {seconds} seconds until the wrapup completes')
@when('I wait {seconds} seconds while being logged on')
@when('I wait {seconds} seconds')
def when_i_wait_n_seconds(context, seconds):
    _sleep(seconds)


def _sleep(seconds):
    time.sleep(float(seconds))
