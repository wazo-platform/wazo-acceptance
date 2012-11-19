# -*- coding: utf-8 -*-
from lettuce import step

from xivo_lettuce.manager_ws import user_manager_ws


@step(u'Given there is a call center supervisor "([^"]*)" "([^"]*)"')
def given_there_is_a_call_center_supervisor_firstname_lastname(step, firstname, lastname):
    user_data = {
        'firstname': firstname,
        'lastname': lastname,
        'client_profile': 'agentsup',
        'client_username': firstname.lower(),
        'client_password': lastname.lower(),
        'enable_client': True,
    }
    user_manager_ws.add_or_replace_user(user_data)
