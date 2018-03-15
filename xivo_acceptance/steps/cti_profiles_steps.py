# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from lettuce import step
from lettuce.registry import world

from xivo_acceptance.helpers import cti_profile_helper, user_helper


@step(u'When I activate the CTI client for user "([^"]*)" "([^"]*)"$')
def when_i_activate_the_cti_client_for_user_group1_group2(step, firstname, lastname):
    user_helper.enable_cti_client(firstname, lastname)


@step(u'When I associate CTI profile with name "([^"]*)" with user "([^"]*)" "([^"]*)"')
def when_i_associate_cti_profile_with_name_group1_with_user_group2_group3(step, cti_profile_name, firstname, lastname):
    cti_profile = {'id': cti_profile_helper.get_id_with_name(cti_profile_name)}
    user = user_helper.get_by_firstname_lastname(firstname, lastname)
    world.confd_client.users(user).update_cti_profile(cti_profile, enabled=False)
