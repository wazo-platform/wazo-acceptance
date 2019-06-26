# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import then

from hamcrest import (
    assert_that,
    has_entries,
    has_item
)


@then('I have the following hints')
def then_i_have_the_following_hints(context):
    output = context.helpers.asterisk.send_to_asterisk_cli('core show hints').split('\n')
    output = output[2:-3]  # strip header and footer
    hints = [{'exten': line[:20].strip(), 'line': line[22:44].strip()}
             for line in output]

    for row in context.table:
        row = row.as_dict()
        assert_that(hints, has_item(has_entries(row)))
