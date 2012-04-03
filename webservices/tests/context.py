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

import unittest, json
from webservices.webservices import WebServices


class TestContext(unittest.TestCase):
    def setUp(self):
        self._aws = WebServices('ipbx/system_management/context')
        response = self._aws.view('toto')
        if response:
            self._aws.delete('toto')

    def tearDown(self):
        pass

    def test_add(self):
        var_replace = {
                      "name": 'toto',
                      "displayname" : 'Toto Corp.',
                      "entity" : 'avencall',
                      "contexttype": 'internal',
                      "contextinclude": '[]',
                      "contextnumbers_user": '"user": [{"numberbeg": "600", "numberend": "699"}]',
                      "contextnumbers_group": '',
                      "contextnumbers_meetme": '',
                      "contextnumbers_queue": '',
                      "contextnumbers_incall": ''
                      }
        jsonfilecontent = self._aws.get_json_file_content('context');
        jsonstr = jsonfilecontent % (var_replace)
        content = json.loads(jsonstr)

        response = self._aws.add(content)
        self.assertEqual(response.code, 200)

        response = self._aws.view(var_replace['name'])
        self.assertEqual(response.code, 200)
        return var_replace['name']

    def test_delete(self):
        id = self.test_add()
        response = self._aws.delete(id)
        self.assertEqual(response.code, 200)
        response = self._aws.search('toto')
        self.assertEqual(response.code, 204)


if __name__ == '__main__':
    unittest.main()
