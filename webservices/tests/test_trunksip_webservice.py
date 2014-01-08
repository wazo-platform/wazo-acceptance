# -*- coding: utf-8 -*-

# Copyright (C) 2012-2014 Avencall
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

    def test_add_trunksip(self):
        trunksip = xivo_ws.SIPTrunk()
        trunksip.name = u'test_ws_add_trunksip'
        trunksip.context = u'default'
        common.delete_with_name('sip_trunks', trunksip.name)
        self._xivo_ws.sip_trunks.add(trunksip)

        self.assertEqual(common.nb_with_name('sip_trunks', trunksip.name), 1)

    def test_edit_trunksip(self):
        common.delete_with_name('sip_trunks', u'test_ws_edit_trunksip')
        self._add_trunksip(u'test_ws_add_trunksip')
        trunksip = common.find_with_name('sip_trunks', u'test_ws_add_trunksip')[0]
        trunksip.name = u'test_ws_edit_trunksip'
        trunksip.context = u'default'
        self._xivo_ws.sip_trunks.edit(trunksip)
        trunksip = common.find_with_name('sip_trunks', u'test_ws_edit_trunksip')[0]

        self.assertEqual(trunksip.name, u'test_ws_edit_trunksip')

    def test_delete_trunksip(self):
        self._add_trunksip(u'test_ws_delete_trunksip')
        common.delete_with_name('sip_trunks', u'test_ws_delete_trunksip')

        self.assertEqual(common.nb_with_name('sip_trunks', u'test_ws_delete_trunksip'), 0)

    def _add_trunksip(self, name, context='default'):
        common.delete_with_name('sip_trunks', name)
        trunksip = xivo_ws.SIPTrunk()
        trunksip.name = name
        trunksip.context = context
        self._xivo_ws.sip_trunks.add(trunksip)
