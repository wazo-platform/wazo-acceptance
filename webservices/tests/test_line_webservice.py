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

import unittest
import xivo_ws
import common


class TestLineWebServices(unittest.TestCase):

    def setUp(self):
        self._xivo_ws = common.xivo_server_ws

    def test_01_add_sip(self):
        sip_line = xivo_ws.Line(protocol=u'sip')
        sip_line.name = u'name_test_ws_add_sip'
        common.delete_with_name('lines', sip_line.name)
        self._xivo_ws.lines.add(sip_line)

        self.assertEqual(common.nb_with_name('lines', sip_line.name), 1)

    def test_02_edit_sip(self):
        sip_line = self._xivo_ws.lines.search_by_name(u'name_test_ws_add_sip')[0]
        sip_line.name = u'name_test_ws_edit_sip'
        self._xivo_ws.lines.edit(sip_line)
        sip_line = self._xivo_ws.lines.search_by_name(u'name_test_ws_edit_sip')[0]

        self.assertEqual(sip_line.name, u'name_test_ws_edit_sip')

    def test_03_delete_sip(self):
        common.delete_with_name('lines', u'name_test_ws_edit_sip')

        self.assertEqual(common.nb_with_name('lines', u'name_test_ws_add_sip'), 0)
        self.assertEqual(common.nb_with_name('lines', u'name_test_ws_edit_sip'), 0)

    def test_04_add_custom(self):
        custom_line = xivo_ws.Line(protocol=u'custom')
        custom_line.name = u'name_test_ws_add_custom'
        custom_line.interface = u'name_test_ws_add_custom'
        common.delete_with_name('lines', custom_line.name)
        self._xivo_ws.lines.add(custom_line)

        self.assertEqual(common.nb_with_name('lines', custom_line.name), 1)

    def test_05_edit_custom(self):
        custom_line = self._xivo_ws.lines.search_by_name(u'name_test_ws_add_custom')[0]
        custom_line.name = u'name_test_ws_edit_custom'
        custom_line.interface = u'name_test_ws_edit_custom'
        self._xivo_ws.lines.edit(custom_line)
        custom_line = self._xivo_ws.lines.search_by_name(u'name_test_ws_edit_custom')[0]

        self.assertEqual(custom_line.name, u'name_test_ws_edit_custom')

    def test_06_delete_custom(self):
        common.delete_with_name('lines', u'name_test_ws_edit_custom')

        self.assertEqual(common.nb_with_name('lines', u'name_test_ws_add_custom'), 0)
        self.assertEqual(common.nb_with_name('lines', u'name_test_ws_edit_custom'), 0)
