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


class TestEntityWebServices(unittest.TestCase):

    def setUp(self):
        self._xivo_ws = common.xivo_server_ws

    def test_add_entity(self):
        entity = xivo_ws.Entity()
        entity.name = u'test_ws_add_entity'
        entity.display_name = u'test_ws_add_entity'
        common.delete_with_name('entities', entity.name)
        self._xivo_ws.entities.add(entity)

        self.assertEqual(common.nb_with_name('entities', entity.name), 1)

    def test_edit_entity(self):
        common.delete_with_name('entities', u'test_ws_edit_entity')
        self._add_entity(u'test_ws_add_entity')
        entity = common.find_with_name('entities', u'test_ws_add_entity')[0]
        entity.name = u'test_ws_edit_entity'
        entity.display_name = u'test_ws_edit_entity'
        self._xivo_ws.entities.edit(entity)
        entity = common.find_with_name('entities', u'test_ws_edit_entity')[0]

        self.assertEqual(entity.name, u'test_ws_edit_entity')

    def test_delete_entity(self):
        self._add_entity(u'test_ws_delete_entity')
        common.delete_with_name('entities', u'test_ws_delete_entity')

        self.assertEqual(common.nb_with_name('entities', u'test_ws_delete_entity'), 0)

    def _add_entity(self, name):
        common.delete_with_name('entities', name)
        entity = xivo_ws.Entity()
        entity.name = name
        entity.display_name = name
        self._xivo_ws.entities.add(entity)
        entity = common.find_with_name('entities', name)[0]
        return entity.id
