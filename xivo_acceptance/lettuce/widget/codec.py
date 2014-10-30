# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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

import time
from lettuce import world
from xivo_acceptance.lettuce.form.checkbox import Checkbox
from xivo_acceptance.lettuce.form.list_pane import ListPane


class CodecWidget(object):
    '''Wraps the "codecs" customization widget'''

    DEFAULT_FIELDSET_ID = 'fld-codeclist'

    def __init__(self, fieldset_id=DEFAULT_FIELDSET_ID):
        base = world.browser.find_element_by_id(fieldset_id)
        self._checkbox = Checkbox(base.find_element_by_id('it-codec-active'))
        self._pane = ListPane(base.find_element_by_id('codeclist'))

    def customize(self, codecs):
        self._checkbox.check()
        self._pane.remove_all()
        for codec in codecs:
            self._pane.add(codec)
            time.sleep(0.5)

    def uncustomize(self):
        self._pane.remove_all()
        self._checkbox.uncheck()

    def add(self, codec):
        self._checkbox.check()
        self._pane.add(codec)

    def remove(self, codec):
        self._pane.remove(codec)
