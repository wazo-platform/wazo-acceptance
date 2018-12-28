# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from lettuce import step

from xivo_acceptance.helpers import user_line_extension_helper as ule_helper


@step(u'Given there is a call center supervisor:$')
def given_there_is_a_call_center_supervisor(step):
    '''Required columns:

    - firstname
    - lastname
    - cti_login
    - cti_passwd
    '''
    for user_hash in step.hashes:
        user_data = {
            'firstname': user_hash['firstname'],
            'lastname': user_hash['lastname'],
            'client_profile': 'Supervisor',
            'client_username': user_hash['cti_login'],
            'client_password': user_hash['cti_passwd'],
            'enable_client': True,
        }
        ule_helper.add_or_replace_user(user_data, step=step)
