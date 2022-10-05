# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import then
from hamcrest import (
    assert_that,
    has_entries,
)


@then('the wizard is correctly setup')
def then_the_wizard_is_correctly_setup(context):
    response = context.confd_client.wizard.get()
    assert_that(
        response,
        has_entries(
            configured=True,
            configurable=True,
        ),
    )
