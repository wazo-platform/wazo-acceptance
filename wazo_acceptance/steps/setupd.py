# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import when


@when('I pass the setup')
def when_i_pass_the_setup(context):
    body = {
        'engine_internal_address': '192.168.32.240',
        'engine_language': 'en_US',
        'engine_password': 'wazosecret',
        'engine_license': True,
    }
    context.setupd_client.setup.create(body)


@when('I pass the setup with "{setup_language}" as default language')
def when_i_pass_the_setup_with_specific_language(context, setup_language):
    body = {
        'engine_internal_address': '192.168.32.240',
        'engine_language': setup_language,
        'engine_password': 'wazosecret',
        'engine_license': True,
    }
    context.setupd_client.setup.create(body)
