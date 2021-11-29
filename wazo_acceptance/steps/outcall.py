# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given
from wazo_test_helpers import until


@given('there is an outcall using extension "{exten}@{exten_context}"')
def given_there_is_an_outcall_using_extension(context, exten, exten_context):
    outcall_name = f'outcall-{exten}'
    body = {
        'name': outcall_name,
        'enabled': True,
    }
    outcall = context.helpers.outcall.create(body)

    body = {'context': exten_context}
    trunk = context.helpers.trunk.create(body)
    context.helpers.outcall.add_trunk(outcall, trunk)

    template = context.helpers.endpoint_sip.get_template_by(label='global')
    body = {
        'name': outcall_name,
        'auth_section_options': [
            ['username', outcall_name],
            ['password', outcall_name],
        ],
        'endpoint_section_options': [],
        'templates': [template],
    }
    sip = context.helpers.endpoint_sip.create(body)

    context.helpers.trunk.add_endpoint_sip(trunk, sip)
    body = {'exten': exten, 'context': exten_context}
    extension = context.helpers.extension.create(body)

    context.helpers.outcall.add_extension(outcall, extension)

    phone = context.helpers.sip_phone.register_and_track_phone(outcall_name, sip)
    until.true(phone.is_registered, tries=3)
