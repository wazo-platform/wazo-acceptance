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


class TestGroupWebServices(unittest.TestCase):

    def setUp(self):
        self._xivo_ws = common.xivo_server_ws

    def test_01_add_group(self):
        group = xivo_ws.Group()
        group.name = u'name_test_ws_add_group'
        group.context = u'default'
        common.delete_with_name('groups', group.name)
        self._xivo_ws.groups.add(group)

        self.assertEqual(common.nb_with_name('groups', group.name), 1)

    def test_02_edit_group(self):
        group = common.find_with_name('groups', u'name_test_ws_add_group')[0]
        group.name = u'name_test_ws_edit_group'
        group.context = u'default'
        self._xivo_ws.groups.edit(group)
        group = common.find_with_name('groups', u'name_test_ws_edit_group')[0]

        self.assertEqual(group.name, u'name_test_ws_edit_group')

    def test_03_delete_group(self):
        common.delete_with_name('groups', u'name_test_ws_edit_group')

        self.assertEqual(common.nb_with_name('groups', u'name_test_ws_add_group'), 0)
        self.assertEqual(common.nb_with_name('groups', u'name_test_ws_edit_group'), 0)
