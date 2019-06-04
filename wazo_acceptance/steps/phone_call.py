# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from behave import step, when


@step('"{firstname} {lastname}" calls "{exten}"')
def a_calls_exten(context, firstname, lastname, exten):
    user = context.helpers.user.get_by(firstname=firstname, lastname=lastname)
    phone = context.phone_register.get_user_phone(user['uuid'])
    phone.call(exten)


@step('"{firstname} {lastname}" is ringing')
def user_is_ringing(context, firstname, lastname):
    user = context.helpers.user.get_by(firstname=firstname, lastname=lastname)
    phone = context.phone_register.get_user_phone(user['uuid'])
    context.helpers.common.wait_until(phone.is_ringing, tries=3)


@when('I wait "{seconds}" seconds for the call to be forwarded')
@when('I wait "{seconds}" seconds for the timeout to not expire')
def given_i_wait_n_seconds(context, seconds):
    _sleep(seconds)


def _sleep(seconds):
    time.sleep(float(seconds))
