# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

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
