# -*- coding: UTF-8 -*-

import time
from lettuce.decorators import step
from xivo_lettuce import common
from lettuce.registry import world
from selenium.webdriver.common.by import By


@step(u'When i edit CTI Profile "([^"]*)"')
def when_i_edit_cti_profile_group1(step, profile_name):
    common.open_url('profile', 'list')
    common.edit_line(profile_name)
    time.sleep(world.timeout)


@step(u'Then i see default services activated')
def then_i_see_default_services_activated(step):
    services = world.browser.find_element_by_id('it-services').find_elements(By.TAG_NAME, 'option')
    expected_elements = ['enablednd', 'fwdunc', 'fwdbusy', 'fwdrna']
    elements = []
    for service in services:
        value = service.get_attribute("value")
        elements.append(value)

    assert elements == expected_elements, 'missing service in profile client'
