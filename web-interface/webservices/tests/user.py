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


class TestUser(unittest.TestCase):
    def setUp(self):
        self._aws = WebServices(wsobj='users')
        self._aws.deleteall()

    def tearDown(self):
        pass

    def test_add(self):
        with open(self._aws.basepath + '/user.json') as fobj:
            jsonfilecontent = fobj.read()
            jsonstr = jsonfilecontent % ({"firstname": 'Bob',
                                          "lastname" : 'Marley'})
            content = json.loads(jsonstr)

        (code, data) = self._aws.add(content)
        self.assertEqual(code, 200)

        (code, data) = self._aws.list()
        self.assertEqual(code, 200)
        res = json.loads(data)
        self.assertEqual(len(res), 1)
        if 'id' in res[0]:
            return res[0]['id']

    def test_edit(self):
        id = self.test_add()

        with open(self._aws.basepath + '/user.json') as fobj:
            jsonfilecontent = fobj.read()
            jsonstr = jsonfilecontent % ({"firstname": 'Bob',
                                          "lastname" : 'Dylan'})
            content = json.loads(jsonstr)

        (code, data) = self._aws.edit(content, id)
        self.assertEqual(code, 200)

        (code, data) = self._aws.list()
        self.assertEqual(code, 200)
        res = json.loads(data)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['firstname'], 'Bob')
        self.assertEqual(res[0]['lastname'], 'Dylan')

    def test_delete(self):
        id = self.test_add()
        (code, data) = self._aws.delete(id)
        self.assertEqual(code, 200)
        (code, data) = self._aws.list()
        self.assertEqual(code, 204)


if __name__ == '__main__':
    unittest.main()
