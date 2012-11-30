# -*- coding: UTF-8 -*-

import time
from lettuce import step, world
from hamcrest import assert_that, equal_to
from xivo_lettuce import common
from xivo_lettuce.manager import profile_manager


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
    selected_services = profile_manager.selected_services()

    assert_that(selected_services, equal_to(expected_services))
