# -*- coding: utf-8 -*-

__license__ = """
    Copyright (C) 2011  Avencall

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA..
"""

import unittest
import json
from webservices.common import WSCommon


class TestUser(unittest.TestCase):
    def setUp(self):
        self._aws_user = WSCommon('ipbx/pbx_settings/users')
        self._aws_lines = WSCommon('ipbx/pbx_settings/lines')

    def test_add(self):
        user_names = ('Mark', 'Vance')
        self._remove_users(*user_names)

        user = self._add_user(*user_names)
        self.assertNotEqual(user, None, 'Unable to add user')

    def test_edit(self):
        user_names = ('Bob', 'Marley')
        changed_names = ('Boby', 'Dylan')
        self._remove_users(*user_names)
        self._remove_users(*changed_names)
        user = self._add_user(*user_names)
        added_user_id = user['userfeatures']['id']

        mod_user_json = self._new_user(*changed_names)

        self.assertTrue(self._aws_user.edit(added_user_id, mod_user_json))

        user = self._get_user(*changed_names)
        self.assertEqual(user['userfeatures']['id'], added_user_id)
        self.assertEqual(user['userfeatures']['firstname'], 'Boby')
        self.assertEqual(user['userfeatures']['lastname'], 'Dylan')

    def test_delete(self):
        user_names = ('Alice', 'DeleteName')
        self._remove_users(*user_names)
        user = self._add_user(*user_names)
        self.assertTrue(self._aws_user.simple_delete(user['userfeatures']['id']))
        user = self._get_user(*user_names)
        self.assertEqual(user, None, 'Unable to delete user')

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

    def _new_user(self, firstname, lastname):
        return {
                "userfeatures": {
                    "entityid": 1,
                    "firstname": unicode(firstname),
                    "lastname": unicode(lastname),
                 },
        }

    def _get_user(self, firstname, lastname):
        users = self._aws_user.list()
        if users is not None:
            matching_users = [user for user in users if user['firstname'] == firstname and user['lastname'] == lastname]
        if len(matching_users) == 1:
            user = self._aws_user.view(matching_users[0]['id'])
            return user
        else:
            return None

    def _add_user(self, firstname, lastname):
        user_json = self._new_user(firstname, lastname)
        self._aws_user.simple_add(user_json)
        user = self._get_user(firstname, lastname)
        return user

    def _remove_users(self, firstname, lastname):
        users = self._aws_user.list()
        if users is not None:
            matching_users = [user for user in users if user['firstname'] == firstname and user['lastname'] == lastname]
        for user in matching_users:
            self._aws_user.simple_delete(user['id'])

    def _new_line(self, name, secret):
        return {
                "protocol": {
                             "name": unicode(name),
                             "secret": unicode(secret),
                             "protocol": "sip",
                             "context": "default"
                             },
                }

    def _add_line(self, name, secret):
        line_json = self._new_line(name, secret)
        self._aws_lines.simple_add(line_json)
        line = self._get_line(name)
        return line

    def _get_line(self, name):
        lines = self._aws_lines.list()
        if lines is not None:
            matching_lines = [line for line in lines if line['name'] == name]
        if len(matching_lines) == 1:
            return matching_lines[0]
        else:
            return None

if __name__ == '__main__':
    unittest.main()
