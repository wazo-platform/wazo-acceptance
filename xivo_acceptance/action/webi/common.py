# -*- coding: utf-8 -*-
# Copyright 2014-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import world
from selenium.webdriver.common.action_chains import ActionChains


def reset_focus():
    non_interactive = world.browser.find_element_by_id("logo")
    ActionChains(world.browser).move_to_element(non_interactive).perform()
    non_interactive.click()
