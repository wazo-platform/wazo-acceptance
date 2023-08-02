# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import when


@when('I set the following options in endpoint sip "{exten}@{exten_context}"')
def when_i_set_the_following_option_in_endpoint_sip(context, exten, exten_context):
    context_name = context.helpers.context.get_by(label=exten_context)['name']
    for row in context.table:
        row = row.as_dict()
        extension = context.helpers.extension.find_by(
            exten=exten,
            context=context_name
        )
        line_id = extension['lines'][0]['id']
        line = context.confd_client.lines.get(line_id)
        sip = context.confd_client.endpoints_sip.get(line['endpoint_sip'])

        for option, value in sip['auth_section_options']:
            if option in row.keys():
                sip['auth_section_options'].remove([option, value])

        body = {
            'uuid': sip['uuid'],
            'auth_section_options': sip['auth_section_options'],
        }

        for option, value in row.items():
            if option == 'username':
                body['name'] = value
                body['auth_section_options'].append([option, value])

        context.helpers.endpoint_sip.update(body)
