# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

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
