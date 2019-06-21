# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import then
from behave import when

from hamcrest import assert_that
from hamcrest import has_entries
from hamcrest import has_item


@when(u'I update lines with infos')
def when_i_update_lines_with_infos(context):
    for row in context.table:
        row = dict(zip(row.headings, row.cells))
        exten = row.pop('exten')
        exten_context = row.pop('context')
        extension = context.helpers.extension.find_by(
            exten=exten,
            context=exten_context
        )
        line_id = extension['lines'][0]['id']
        line = context.confd_client.lines.get(line_id)
        sip = {
            "id": line['endpoint_sip']['id']
        }
        for option, value in row.items():
            sip[option] = value
        context.confd_client.endpoints_sip.update(sip)


@then('I have the following hints')
def then_i_have_the_following_hints(context):
    output = context.helpers.asterisk.send_to_asterisk_cli('core show hints').split('\n')
    output = output[2:-3]  # strip header and footer
    hints = [{'exten': line[:20].strip(), 'line': line[22:44].strip()}
             for line in output]

    for row in context.table:
        row = dict(zip(row.headings, row.cells))
        assert_that(hints, has_item(has_entries(row)))
