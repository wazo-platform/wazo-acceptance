# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from lettuce import step

from xivo_acceptance.helpers import user_line_extension_helper as ule_helper


@step(u'Given there is a call center supervisor "([^"]*)" "([^"]*)"')
def given_there_is_a_call_center_supervisor_firstname_lastname(step, firstname, lastname):
    user_data = {
        'firstname': firstname,
        'lastname': lastname,
        'client_profile': 'Supervisor',
        'client_username': firstname.lower(),
        'client_password': lastname.lower(),
        'enable_client': True,
    }
    ule_helper.add_or_replace_user(user_data, step=step)
