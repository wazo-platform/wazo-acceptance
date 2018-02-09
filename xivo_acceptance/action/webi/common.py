# -*- coding: UTF-8 -*-
# Copyright (C) 2014 Avencall
# SPDX-License-Identifier: GPL-3.0+


import time

from lettuce import world


def reset_focus():
    non_interactive = world.browser.find_element_by_id("logo")
    time.sleep(1)
    non_interactive.click()
