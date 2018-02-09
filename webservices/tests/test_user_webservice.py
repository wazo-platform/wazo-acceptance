# -*- coding: utf-8 -*-
# Copyright (C) 2012-2016 Avencall
# SPDX-License-Identifier: GPL-3.0+

import xivo_ws
import unittest
import common


class TestUserWebServices(unittest.TestCase):

    def setUp(self):
        self._xivo_ws = common.xivo_server_ws

    def test_add_user(self):
        user = xivo_ws.User()
        user.firstname = u'test_ws_add_user'
        common.delete_with_firstname_lastname('users', user.firstname, '')
        self._xivo_ws.users.add(user)

        self.assertEqual(common.nb_with_firstname_lastname('users', user.firstname, ''), 1)

    def test_edit_user(self):
        common.delete_with_firstname_lastname('users', u'test_ws_edit_user', '')
        self._add_user(u'test_ws_add_user', '')
        user = common.find_with_firstname_lastname('users', u'test_ws_add_user', '')[0]
        user.firstname = u'test_ws_edit_user'
        self._xivo_ws.users.edit(user)
        user = common.find_with_firstname_lastname('users', u'test_ws_edit_user', '')[0]

        self.assertEqual(user.firstname, u'test_ws_edit_user')

    def test_delete_user(self):
        self._add_user(u'test_ws_delete_user', '')
        common.delete_with_firstname_lastname('users', u'test_ws_delete_user', '')

        self.assertEqual(common.nb_with_firstname_lastname('users', u'test_ws_delete_user', ''), 0)

    def _add_user(self, firstname, lastname):
        common.delete_with_firstname_lastname('users', firstname, lastname)
        user = xivo_ws.User()
        user.firstname = firstname
        user.lastname = lastname
        self._xivo_ws.users.add(user)
        user = common.find_with_firstname_lastname('users', firstname, lastname)[0]
        return user.id
