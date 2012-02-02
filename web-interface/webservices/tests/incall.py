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
from webservices.webservices import WebServicesFactory


class TestIncall(unittest.TestCase):
    def setUp(self):
        self._aws = WebServices('incall')
        self._aws.deleteall()

    def tearDown(self):
        pass

    def test_add(self):
        var_context = {
                      "name": 'toto',
                      "displayname" : 'Toto Corp.',
                      "entity" : 'avencall',
                      "contexttype": 'incall',
                      "contextinclude": '[]',
                      "contextnumbers_user": '',
                      "contextnumbers_group": '',
                      "contextnumbers_meetme": '',
                      "contextnumbers_queue": '',
                      "contextnumbers_incall": '"incall": [{"numberbeg": "5000", "numberend": "6000", "didlength": "4"}]'
                      }
        jsonfilecontent = self._aws.get_json_file_content('context');
        jsonstr = jsonfilecontent % (var_context)
        data = json.loads(jsonstr)
        wsctx = WebServicesFactory('context')
        wsctx.delete('toto')
        wsctx.add(data)
        
        var_incall = {
                      "exten": '5000',
                      "context" : var_context['name']
                      }
        jsonfilecontent = self._aws.get_json_file_content('incall');
        jsonstr = jsonfilecontent % (var_incall)
        content = json.loads(jsonstr)

        response = self._aws.add(content)
        self.assertEqual(response.code, 200)

        response = self._aws.search(var_incall['exten'])
        self.assertEqual(response.code, 200)
        wsctx.delete(var_context['name'])
        res = json.loads(response.data)
        self.assertEqual(len(res), 1)
        if 'id' in res[0]:
            return res[0]['id']

    def test_delete(self):
        id = self.test_add()
        response = self._aws.delete(id)
        self.assertEqual(response.code, 200)
        response = self._aws.list()
        self.assertEqual(response.code, 204)


if __name__ == '__main__':
    unittest.main()
