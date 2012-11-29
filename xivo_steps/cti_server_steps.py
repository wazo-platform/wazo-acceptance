# -*- coding: UTF-8 -*-

import time
from lettuce import step, world
from hamcrest import assert_that, equal_to
from xivo_lettuce import common
from xivo_lettuce.form.list_pane import ListPane


@step(u'When i edit CTI Profile "([^"]*)"')
def when_i_edit_cti_profile_group1(step, profile_name):
    common.open_url('profile', 'list')
    common.edit_line(profile_name)
    time.sleep(world.timeout)


@step(u'Then I see default services activated')
def then_i_see_default_services_activated(step):
    expected_labels = [
        'Enable DND',
        'Unconditional transfer to a number',
        'Transfer on busy',
        'Transfer on no-answer',
    ]
    list_pane = ListPane.from_id('queuelist')

    assert_that(list_pane.selected_labels(), equal_to(expected_labels))
