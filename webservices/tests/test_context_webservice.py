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


class TestContextWebServices(unittest.TestCase):

    def setUp(self):
        self._xivo_ws = common.xivo_server_ws

    def test_add_context(self):
        context = xivo_ws.Context()
        context.entity = 1
        context.name = u'test_ws_add_context'
        context.display_name = u'test_ws_add_context'
        self._delete_context(context.name)
        self._xivo_ws.contexts.add(context)

        self.assertEqual(common.nb_with_name('contexts', context.name), 1)

    def test_edit_context(self):
        common.delete_with_name('contexts', u'test_ws_edit_context')
        self._add_context(u'test_ws_add_context')
        context = common.find_with_name('contexts', u'test_ws_add_context')[0]
        context.name = u'test_ws_edit_context'
        context.display_name = u'test_ws_edit_context'
        self._xivo_ws.contexts.edit(context)
        context = common.find_with_name('contexts', u'test_ws_edit_context')[0]

        self.assertEqual(context.name, u'test_ws_edit_context')

    def test_delete_context(self):
        self._add_context(u'test_ws_delete_context')
        common.delete_with_name('contexts', u'test_ws_delete_context')

        self.assertEqual(common.nb_with_name('contexts', u'test_ws_delete_context'), 0)

    def _add_context(self, name):
        common.delete_with_name('contexts', name)
        context = xivo_ws.Context()
        context.entity = 1
        context.name = name
        context.display_name = name
        self._xivo_ws.contexts.add(context)

    def _delete_context(self, name):
        common.delete_with_name('contexts', name)
