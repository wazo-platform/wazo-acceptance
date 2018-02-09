# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

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
        self._add_context(u'test_ws_edit_context')
        context = common.find_with_name('contexts', u'test_ws_edit_context')[0]
        context.display_name = u'foobar'
        self._xivo_ws.contexts.edit(context)
        context = common.find_with_name('contexts', u'test_ws_edit_context')[0]

        self.assertEqual(context.display_name, u'foobar')

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
