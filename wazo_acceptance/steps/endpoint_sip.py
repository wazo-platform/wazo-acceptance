# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import when


@when('I set the following options in endpoint sip "{exten}@{exten_context}"')
def when_i_set_the_following_option_in_endpoint_sip(context, exten, exten_context):
    for row in context.table:
        row = row.as_dict()
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
        context.helpers.endpoint_sip.update(sip)