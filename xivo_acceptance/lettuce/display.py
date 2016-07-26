# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

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
