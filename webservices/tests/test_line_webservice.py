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

    def test_add_sip(self):
        sip_line = xivo_ws.Line(protocol=u'sip')
        sip_line.name = u'test_ws_add_sip'
        common.delete_with_name('lines', sip_line.name)
        self._xivo_ws.lines.add(sip_line)

        self.assertEqual(common.nb_with_name('lines', sip_line.name), 1)

    def test_edit_sip(self):
        common.delete_with_name('lines', u'test_ws_edit_sip')
        self._add_sip_line(u'test_ws_add_sip')
        sip_line = self._xivo_ws.lines.search_by_name(u'test_ws_add_sip')[0]
        sip_line.name = u'test_ws_edit_sip'
        self._xivo_ws.lines.edit(sip_line)
        sip_line = self._xivo_ws.lines.search_by_name(u'test_ws_edit_sip')[0]

        self.assertEqual(sip_line.name, u'test_ws_edit_sip')

    def test_delete_sip(self):
        self._add_sip_line(u'test_ws_delete_sip')
        common.delete_with_name('lines', u'test_ws_delete_sip')

        self.assertEqual(common.nb_with_name('lines', u'test_ws_delete_sip'), 0)

    def test_add_custom(self):
        custom_line = xivo_ws.Line(protocol=u'custom')
        custom_line.name = u'test_ws_add_custom'
        custom_line.interface = u'test_ws_add_custom'
        common.delete_with_name('lines', custom_line.name)
        self._xivo_ws.lines.add(custom_line)

        self.assertEqual(common.nb_with_name('lines', custom_line.name), 1)

    def test_edit_custom(self):
        common.delete_with_name('lines', u'test_ws_edit_custom')
        self._add_custom_line(u'test_ws_add_custom', u'test_ws_add_custom')
        custom_line = self._xivo_ws.lines.search_by_name(u'test_ws_add_custom')[0]
        custom_line.name = u'test_ws_edit_custom'
        custom_line.interface = u'test_ws_edit_custom'
        self._xivo_ws.lines.edit(custom_line)
        custom_line = self._xivo_ws.lines.search_by_name(u'test_ws_edit_custom')[0]

        self.assertEqual(custom_line.name, u'test_ws_edit_custom')
        self.assertEqual(custom_line.interface, u'test_ws_edit_custom')

    def test_delete_custom(self):
        self._add_custom_line(u'test_ws_delete_custom', u'test_ws_delete_custom')
        common.delete_with_name('lines', u'test_ws_delete_custom')

        self.assertEqual(common.nb_with_name('lines', u'test_ws_delete_custom'), 0)

    def _add_sip_line(self, name):
        common.delete_with_name('lines', name)
        sip_line = xivo_ws.Line(protocol=u'sip')
        sip_line.name = name
        common.delete_with_name('lines', sip_line.name)
        self._xivo_ws.lines.add(sip_line)

    def _add_custom_line(self, name, interface):
        common.delete_with_name('lines', name)
        custom_line = xivo_ws.Line(protocol=u'custom')
        custom_line.name = name
        custom_line.interface = interface
        self._xivo_ws.lines.add(custom_line)
