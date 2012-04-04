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


class TestLine(unittest.TestCase):
    def setUp(self):
        self._aws = WebServices('ipbx/pbx_settings/lines')
        self._aws.deleteall()

    def tearDown(self):
        self._aws.deleteall()

    def test_add_sip(self):
        jsonfilecontent = self._aws.get_json_file_content('linesip');
        jsonstr = jsonfilecontent % ({"name": 'name',
                                      "secret" : 'secret'})
        content = json.loads(jsonstr)
        return self._add(content)

    def test_edit_sip(self):
        jsonfilecontent = self._aws.get_json_file_content('linesip');
        jsonstr = jsonfilecontent % ({"name": 'name2',
                                      "secret" : 'secret2'})
        content = json.loads(jsonstr)
        id = self.test_add_sip()
        self._edit(id, content)
        response = self._aws.list()
        self.assertEqual(response.code, 200)
        res = json.loads(response.data)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['name'], 'name2')
        self.assertEqual(res[0]['secret'], 'secret2')

    def test_delete_sip(self):
        id = self.test_add_sip()
        self._delete(id)

    def test_add_custom(self):
        jsonfilecontent = self._aws.get_json_file_content('linecustom');
        jsonstr = jsonfilecontent % ({"interface": 'dahdi/g1'})
        content = json.loads(jsonstr)
        return self._add(content)

    def test_edit_custom(self):
        jsonfilecontent = self._aws.get_json_file_content('linecustom');
        jsonstr = jsonfilecontent % ({"interface": 'dahdi/g2'})
        content = json.loads(jsonstr)
        id = self.test_add_custom()
        self._edit(id, content)
        response = self._aws.list()
        self.assertEqual(response.code, 200)
        res = json.loads(response.data)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['interface'], 'dahdi/g2')

    def test_delete_custom(self):
        id = self.test_add_custom()
        self._delete(id)

    def _add(self, content):
        response = self._aws.add(content)
        self.assertEqual(response.code, 200)
        response = self._aws.list()
        self.assertEqual(response.code, 200)
        res = json.loads(response.data)
        self.assertEqual(len(res), 1)
        if 'id' in res[0]:
            return res[0]['id']

    def _edit(self, id, content):
        response = self._aws.edit(content, id)
        self.assertEqual(response.code, 200)

    def _delete(self, id):
        response = self._aws.delete(id)
        self.assertEqual(response.code, 200)
        response = self._aws.list()
        self.assertEqual(response.code, 204)


if __name__ == '__main__':
    unittest.main()
