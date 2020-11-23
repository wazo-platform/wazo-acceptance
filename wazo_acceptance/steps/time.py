# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from behave import given
from datetime import datetime, timedelta


@given('there are no hour change in the next {seconds} seconds')
def no_hour_change_in_next_1_seconds(context, seconds):
    now = datetime.now()
    delta_until_next_hour = timedelta(hours=1) - timedelta(minutes=now.minute, seconds=now.second)
    if delta_until_next_hour.total_seconds() < int(seconds):
        time.sleep(seconds)
