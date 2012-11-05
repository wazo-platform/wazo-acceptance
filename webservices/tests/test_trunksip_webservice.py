# -*- coding: utf-8 -*-

# Copyright (C) 2012  Avencall
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

import xivo_ws
import unittest
import common


class TestTrunkSipWebServices(unittest.TestCase):

    def setUp(self):
        self._xivo_ws = common.xivo_server_ws

    def test_01_add_trunksip(self):
        trunksip = xivo_ws.SIPTrunk()
        trunksip.name = u'name_test_ws_add_trunksip'
        trunksip.context = u'default'
        common.delete_with_name('sip_trunks', trunksip.name)
        self._xivo_ws.sip_trunks.add(trunksip)

        self.assertEqual(common.nb_with_name('sip_trunks', trunksip.name), 1)

    def test_02_edit_trunksip(self):
        trunksip = common.find_with_name('sip_trunks', u'name_test_ws_add_trunksip')[0]
        trunksip.name = u'name_test_ws_edit_trunksip'
        trunksip.context = u'default'
        self._xivo_ws.sip_trunks.edit(trunksip)
        trunksip = common.find_with_name('sip_trunks', u'name_test_ws_edit_trunksip')[0]

        self.assertEqual(trunksip.name, u'name_test_ws_edit_trunksip')

    def test_03_delete_trunksip(self):
        common.delete_with_name('sip_trunks', u'name_test_ws_edit_trunksip')

        self.assertEqual(common.nb_with_name('sip_trunks', u'name_test_ws_add_trunksip'), 0)
        self.assertEqual(common.nb_with_name('sip_trunks', u'name_test_ws_edit_trunksip'), 0)
