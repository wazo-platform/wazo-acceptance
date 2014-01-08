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


class TestIncallWebServices(unittest.TestCase):

    def setUp(self):
        self._xivo_ws = common.xivo_server_ws

    def test_add_incall(self):
        self._add_user()
        incall = xivo_ws.Incall()
        incall.number = u'4000'
        incall.context = u'from-extern'
        incall.destination = self._new_user_destination(u'test_ws_user_firstname')
        common.delete_with_number('incalls', incall.number)
        self._xivo_ws.incalls.add(incall)

        self.assertEqual(common.nb_with_number('incalls', incall.number), 1)

    def test_edit_incall(self):
        common.delete_with_number('incalls', u'4001')
        self._add_incall(u'4000')
        incall = common.find_with_number('incalls', u'4000')[0]
        incall.number = u'4001'
        incall.context = u'from-extern'
        incall.destination = self._new_user_destination(u'test_ws_user_firstname')
        self._xivo_ws.incalls.edit(incall)
        incall = common.find_with_number('incalls', u'4001')[0]

        self.assertEqual(incall.number, u'4001')

    def test_delete_incall(self):
        self._add_incall(u'4000')
        common.delete_with_number('incalls', u'4000')
        common.delete_with_firstname_lastname('users', u'test_ws_user_firstname', '')

        self.assertEqual(common.nb_with_number('incalls', u'4000'), 0)

    def _new_user_destination(self, firstname, lastname=''):
        user_id = common.find_with_firstname_lastname('users', firstname, lastname)[0].id
        return xivo_ws.UserDestination(user_id)

    def _add_user(self):
        user = xivo_ws.User()
        user.firstname = u'test_ws_user_firstname'
        common.delete_with_firstname_lastname('users', user.firstname, '')
        self._xivo_ws.users.add(user)

    def _add_incall(self, number):
        self._add_user()
        common.delete_with_number('incalls', number)
        incall = xivo_ws.Incall()
        incall.number = number
        incall.context = u'from-extern'
        incall.destination = self._new_user_destination(u'test_ws_user_firstname')
        self._xivo_ws.incalls.add(incall)
        incall = common.find_with_number('incalls', number)[0]
        return incall.id
