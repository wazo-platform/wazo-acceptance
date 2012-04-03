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
from webservices.common import WSCommon


class TestUser(unittest.TestCase):
    def setUp(self):
        self._aws_user = WSCommon('ipbx/pbx_settings/users')
        self._aws_lines = WSCommon('ipbx/pbx_settings/lines')
        self._aws_user.clear()
        self._aws_lines.clear()

    def tearDown(self):
        self._aws_user.clear()
        self._aws_lines.clear()

    def test_add(self):
        jsonfilecontent = self._aws_user.get_json_file_content('user');
        jsonstr = jsonfilecontent % ({"firstname": 'Bob',
                                      "lastname" : 'Marley'})
        content = json.loads(jsonstr)
        return self._aws_user.add(content)

    def test_edit(self):
        jsonfilecontent = self._aws_user.get_json_file_content('user');
        jsonstr = jsonfilecontent % ({"firstname": 'Bob',
                                      "lastname" : 'Marley'})
        content = json.loads(jsonstr)
        id = self._aws_user.add(content)
        jsonfilecontent = self._aws_user.get_json_file_content('user');
        jsonstr = jsonfilecontent % ({"firstname": 'Boby',
                                      "lastname" : 'Dylan'})
        content = json.loads(jsonstr)
        self.assertTrue(self._aws_user.edit(id, content))

        res = self._aws_user.list()
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['firstname'], 'Boby')
        self.assertEqual(res[0]['lastname'], 'Dylan')

    def test_delete(self):
        jsonfilecontent = self._aws_user.get_json_file_content('user');
        jsonstr = jsonfilecontent % ({"firstname": 'Bob',
                                      "lastname" : 'Marley'})
        content = json.loads(jsonstr)
        id = self._aws_user.add(content)
        self.assertTrue(self._aws_user.delete(id))

    def test_associate_existant_user_with_line(self):
        jsonfilecontent = self._aws_user.get_json_file_content('user');
        jsonstr = jsonfilecontent % ({"firstname": 'Paul',
                                      "lastname" : 'Castagnette'})
        content = json.loads(jsonstr)
        userid = self._aws_user.add(content)
        
        jsonfilecontent = self._aws_lines.get_json_file_content('linesip');
        jsonstr = jsonfilecontent % ({"name": 'name',
                                      "secret" : 'secret'})
        content = json.loads(jsonstr)
        lineid = self._aws_lines.add(content)
        
        jsonfilecontent = self._aws_user.get_json_file_content('user_link_line');
        jsonstr = jsonfilecontent % ({"firstname": 'Paul',
                                      "idlinefeatures" : lineid,
                                      "number" : 177})
        self.assertTrue(self._aws_user.edit(userid, content))


if __name__ == '__main__':
    unittest.main()
