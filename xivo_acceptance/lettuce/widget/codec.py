# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

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
