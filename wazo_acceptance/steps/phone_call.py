# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from xivo_test_helpers import until
from behave import step, when


@step('"{tracking_id}" calls "{exten}"')
def a_calls_exten(context, tracking_id, exten):
    phone = context.phone_register.get_phone(tracking_id)
    phone.call(exten)


@step('"{tracking_id}" is ringing')
def user_is_ringing(context, tracking_id):
    phone = context.phone_register.get_phone(tracking_id)
    until.true(phone.is_ringing, tries=3)


@step('"{tracking_id}" is hungup')
def user_is_hungup(context, tracking_id):
    phone = context.phone_register.get_phone(tracking_id)
    until.true(phone.is_hungup, tries=3)


@when('I wait "{seconds}" seconds for the call to be forwarded')
@when('I wait "{seconds}" seconds for the timeout to not expire')
def given_i_wait_n_seconds(context, seconds):
    _sleep(seconds)


def _sleep(seconds):
    time.sleep(float(seconds))
