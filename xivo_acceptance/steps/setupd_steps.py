# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step, world


@step(u'When I pass the setup')
def when_i_pass_the_setup(step):
    body = {
        'engine_internal_address': '192.168.32.240',
        'engine_language': 'en_US',
        'engine_password': 'wazosecret',
        'engine_license': True,
    }
    world.setupd_client.setup.create(body)
