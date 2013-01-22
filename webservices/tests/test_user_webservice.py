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

    def test_associate_existant_user_with_line(self):
        user_id = self._add_user(u'test_ws_associate_user', 'with_line')
        line_id = self._add_sip_line('test_associate', 'secret')

        user = common.find_with_firstname_lastname('users', u'test_ws_associate_user', u'with_line')[0]
        user.line = xivo_ws.UserLine(id=line_id)
        self._xivo_ws.users.edit(user)

        line = self._xivo_ws.lines.search_by_name(u'test_associate')[0]

        self.assertEqual(user_id, line.user_id)

        common.delete_with_firstname_lastname('users', u'test_ws_associate_user', u'with_line')
        common.delete_with_name('lines', u'test_associate')

    def _add_user(self, firstname, lastname):
        common.delete_with_firstname_lastname('users', firstname, lastname)
        user = xivo_ws.User()
        user.firstname = firstname
        user.lastname = lastname
        self._xivo_ws.users.add(user)
        user = common.find_with_firstname_lastname('users', firstname, lastname)[0]
        return user.id

    def _add_sip_line(self, name, secret, context='default'):
        common.delete_with_name('lines', name)
        line = xivo_ws.Line()
        line.protocol = line.PROTOCOL_SIP
        line.name = name
        line.secret = secret
        line.context = context
        common.delete_with_name('lines', name)
        self._xivo_ws.lines.add(line)
        line = common.find_with_name('lines', name)[0]
        return line.id
