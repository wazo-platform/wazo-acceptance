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
        self._aws = WebServices('ipbx/call_management/incall')
        self.context_name = "test_incall_context"
        self._add_context()

    def tearDown(self):
        pass

    def new_incall_content(self, exten):
        return {
            "incall": {
                "exten": unicode(exten),
                "context": unicode(self.context_name),
                "preprocess_subroutine": "",
            },
            "dialaction": {
                "answer": {
				 "actiontype": "endcall:hangup",
				 "actionarg1": "",
				 "actionarg2": ""
                }
            }
        }


    def test_add(self):
        incall_number = "5000"
        self._delete_incall(incall_number)
        var_incall = self.new_incall_content(incall_number)

        response = self._aws.add(var_incall)
        self.assertEqual(response.code, 200)

        response = self._aws.search(incall_number)
        self.assertEqual(response.code, 200)

    def test_delete(self):
        incall_number = "5100"
        incall_id = self._add_incall(incall_number)

        response = self._aws.delete(incall_id)
        self.assertEqual(response.code, 200)

        response = self._aws.search(incall_number)
        self.assertEqual(response.code, 204)

    def assertIncallActionModified(self, incall_number, action):
        response = self._aws.search(incall_number)
        incalls = json.loads(response.data)
        self.assertEquals(incalls[0]['action'], action, "action not modified")


    def test_edit(self):
        incall_number = "5050"
        incall_id = self._add_incall(incall_number)
        var_incall = self.new_incall_content(incall_number)
        var_incall['dialaction']['answer']['actiontype'] = 'endcall:busy'
        response = self._aws.edit(var_incall, incall_id)
        self.assertEqual(response.code, 200)

        self.assertIncallActionModified(incall_number, "endcall:busy")

    def _delete_incall(self, incall_number):
        response = self._aws.search(incall_number)
        if response.code == 200:
            incalls = json.loads(response.data)
            self._aws.delete(incalls[0]['id'])

    def _add_incall(self, incall_number):
        self._delete_incall(incall_number)
        var_incall = self.new_incall_content(incall_number)
        self._aws.add(var_incall)
        response = self._aws.search(incall_number)
        incalls = json.loads(response.data)
        return incalls[0]['id']

    def _add_context(self):

        var_context = {
                      "name": unicode(self.context_name),
                      "displayname" : "Display %s" % self.context_name,
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
        wsctx = WebServicesFactory('ipbx/system_management/context')
        wsctx.delete(self.context_name)
        wsctx.add(data)
