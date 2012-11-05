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


class TestUserWebServices(unittest.TestCase):

    def setUp(self):
        self._xivo_ws = common.xivo_server_ws

    def test_01_add_user(self):
        user = xivo_ws.User()
        user.firstname = u'name_test_ws_add_user'
        common.delete_with_firstname_lastname('users', user.firstname, '')
        self._xivo_ws.users.add(user)

        self.assertEqual(common.nb_with_firstname_lastname('users', user.firstname, ''), 1)

    def test_02_edit_user(self):
        user = common.find_with_firstname_lastname('users', u'name_test_ws_add_user', '')[0]
        user.firstname = u'name_test_ws_edit_user'
        self._xivo_ws.users.edit(user)
        user = common.find_with_firstname_lastname('users', u'name_test_ws_edit_user', '')[0]

        self.assertEqual(user.firstname, u'name_test_ws_edit_user')

    def test_03_delete_user(self):
        common.delete_with_firstname_lastname('users', u'name_test_ws_edit_user', '')

        self.assertEqual(common.nb_with_firstname_lastname('users', u'name_test_ws_add_user', ''), 0)
        self.assertEqual(common.nb_with_firstname_lastname('users', u'name_test_ws_edit_user', ''), 0)

"""
    def test_associate_existant_user_with_line(self):
        user_names = ('Paul', 'Castagnette')
        self._remove_users(*user_names)
        user = self._add_user(*user_names)
        line = self._add_line('test_associate', 'secret')

        user_json = self._new_user(*user_names)
        user_json["linefeatures"] = {"id": [line['id']]}
        self.assertTrue(self._aws_user.edit(user['userfeatures']['id'], user_json))

        associated_user = self._get_user(*user_names)
        self.assertEqual(associated_user['linefeatures'][0]['id'], line['id'])
"""
