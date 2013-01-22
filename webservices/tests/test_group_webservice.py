# -*- coding: utf-8 -*-

# Copyright (C) 2012-2013 Avencall
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


class TestGroupWebServices(unittest.TestCase):

    def setUp(self):
        self._xivo_ws = common.xivo_server_ws

    def test_add_group(self):
        group = xivo_ws.Group()
        group.name = u'test_ws_add_group'
        group.context = u'default'
        common.delete_with_name('groups', group.name)
        self._xivo_ws.groups.add(group)

        self.assertEqual(common.nb_with_name('groups', group.name), 1)

    def test_edit_group(self):
        common.delete_with_name('groups', u'test_ws_edit_group')
        self._add_group(u'test_ws_add_group')
        group = common.find_with_name('groups', u'test_ws_add_group')[0]
        group.name = u'test_ws_edit_group'
        group.context = u'default'
        self._xivo_ws.groups.edit(group)
        group = common.find_with_name('groups', u'test_ws_edit_group')[0]

        self.assertEqual(group.name, u'test_ws_edit_group')

    def test_delete_group(self):
        self._add_group(u'test_ws_delete_group')
        common.delete_with_name('groups', u'test_ws_delete_group')

        self.assertEqual(common.nb_with_name('groups', u'test_ws_delete_group'), 0)

    def _add_group(self, name, context='default'):
        common.delete_with_name('groups', name)
        group = xivo_ws.Group()
        group.name = name
        group.context = context
        self._xivo_ws.groups.add(group)
        group = common.find_with_name('groups', name)[0]
        return group.id
