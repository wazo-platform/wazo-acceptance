# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import time

from lettuce import step, world
from hamcrest import assert_that, equal_to

from xivo_acceptance.action.webi import profile as profile_action_webi
from xivo_acceptance.lettuce import common


@step(u'Given there is no CTI profile "([^"]*)"$')
def given_there_is_no_cti_profile(step, search):
    common.remove_element_if_exist('CTI profile', search)


@step(u'Then the profile "([^"]*)" has default services activated')
def then_the_profile_1_has_default_services_activated(step, profile_name):
    common.open_url('profile', 'list')
    common.edit_line(profile_name)
    time.sleep(world.timeout)  # wait for the javascript to load

    expected_services = [
        'Enable DND',
        'Unconditional transfer to a number',
        'Transfer on busy',
        'Transfer on no-answer',
    ]
    selected_services = profile_action_webi.selected_services()

    assert_that(selected_services, equal_to(expected_services))
