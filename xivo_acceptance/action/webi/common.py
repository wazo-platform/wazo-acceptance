# -*- coding: utf-8 -*-
# Copyright 2014-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from lettuce import world
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.expected_conditions import visibility_of
from selenium.webdriver.support.ui import WebDriverWait


def reset_focus():
    non_interactive = world.browser.find_element_by_id("logo")
    WebDriverWait(world.browser, world.timeout).until(visibility_of(non_interactive))
    ActionChains(world.browser).move_to_element(non_interactive).perform()
    non_interactive.click()
