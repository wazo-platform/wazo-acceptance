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


class TestContextWebServices(unittest.TestCase):

    def setUp(self):
        self._xivo_ws = common.xivo_server_ws

    def test_01_add_context(self):
        context = xivo_ws.Context()
        context.entity = 1
        context.name = u'name_test_ws_add_context'
        context.display_name = u'name_test_ws_add_context'
        common.delete_with_name('contexts', context.name)
        self._xivo_ws.contexts.add(context)

        self.assertEqual(common.nb_with_name('contexts', context.name), 1)

    def test_02_edit_context(self):
        context = common.find_with_name('contexts', u'name_test_ws_add_context')[0]
        context.name = u'name_test_ws_edit_context'
        context.display_name = u'name_test_ws_edit_context'
        self._xivo_ws.contexts.edit(context)
        context = common.find_with_name('contexts', u'name_test_ws_edit_context')[0]

        self.assertEqual(context.name, u'name_test_ws_edit_context')

    def test_03_delete_context(self):
        common.delete_with_name('contexts', u'name_test_ws_edit_context')

        self.assertEqual(common.nb_with_name('contexts', u'name_test_ws_add_context'), 0)
        self.assertEqual(common.nb_with_name('contexts', u'name_test_ws_edit_context'), 0)
