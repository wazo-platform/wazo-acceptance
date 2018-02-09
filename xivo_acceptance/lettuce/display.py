# -*- coding: utf-8 -*-
# Copyright (C) 2016 Avencall
# SPDX-License-Identifier: GPL-3.0+

from pyvirtualdisplay import Display
from lettuce import world


class XiVODisplay(object):

    def __init__(self):
        self.instance = None

    def get_instance(self):
        if self.instance:
            return self.instance
        return self._set_instance()

    def _set_instance(self):
        browser_size = tuple(world.config['browser']['resolution'].split('x', 1))
        self.instance = Display(visible=world.config['browser']['visible'], size=browser_size)
        return self.instance.start()
