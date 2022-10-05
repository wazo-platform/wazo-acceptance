# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import when
from hamcrest import assert_that, equal_to


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
    sound_file_language = setup_language.lower().replace('_','-')
    sound_file_name = f'asterisk-sounds-wav-{sound_file_language}'
    assert_that(
        context.remote_sysutils.send_command(['apt-get', 'update'], check=True),
        equal_to(True),
    )
    assert_that(
        context.remote_sysutils.send_command(['apt-get', '-y', 'install', sound_file_name], check=True),
        equal_to(True),
    )
    body = {
        'engine_internal_address': '192.168.32.240',
        'engine_language': setup_language,
        'engine_password': 'wazosecret',
        'engine_license': True,
    }
    context.setupd_client.setup.create(body)
