# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from lettuce import world


def type_pool_start_end(start, end):
    input_start = world.browser.find_element_by_id('it-pool_start', 'DHCP form not loaded')
    input_end = world.browser.find_element_by_id('it-pool_end')
    input_start.clear()
    input_start.send_keys(start)
    input_end.clear()
    input_end.send_keys(end)
