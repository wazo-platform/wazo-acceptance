# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from xivo_test_helpers import until
from behave import step, when

CHAN_PREFIX = 'PJSIP'


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


@step('"{tracking_id}" is talking')
def user_is_talking(context, tracking_id):
    phone = context.phone_register.get_phone(tracking_id)
    until.true(phone.is_talking, tries=3)


@when('I wait "{seconds}" seconds for the call processing')
@when('I wait "{seconds}" seconds for the call to be forwarded')
@when('I wait "{seconds}" seconds for the end of ringing time')
@when('I wait "{seconds}" seconds for the timeout to not expire')
def given_i_wait_n_seconds(context, seconds):
    _sleep(seconds)


@when('chan_test calls "{exten}@{exten_context}"')
def when_chan_test_calls(context, exten, exten_context):
    cmd = 'test new {exten} {context} chan-test-num chan-test-name {prefix}'.format(
        exten=exten,
        context=exten_context,
        prefix=CHAN_PREFIX,
    )
    context.helpers.asterisk.send_to_asterisk_cli(cmd)


def _sleep(seconds):
    time.sleep(float(seconds))
