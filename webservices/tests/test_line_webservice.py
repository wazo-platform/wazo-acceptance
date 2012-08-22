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
import xivo_ws
from webservices.webservices import WebServices

class TestLine(unittest.TestCase):
    def setUp(self):
        self._aws = WebServices('ipbx/pbx_settings/lines')
        self._xivo_ws = self._aws.ws

    def tearDown(self):
        pass

    def test_add_sip(self):
        new_sip_line = xivo_ws.Line(protocol=u'sip')
        new_sip_line.name = u'name_test_ws_add_sip'
        self._delete_lines_with_name(new_sip_line.name)

        self._xivo_ws.lines.add(new_sip_line)

        self.assertEqual(self._nb_lines_with_name(new_sip_line.name), 1)

    def _delete_lines_with_name(self, name_to_delete):
        for listed_line in self._lines_with_name(name_to_delete):
            self._xivo_ws.lines.delete(listed_line.id)

        self.assertEqual(self._nb_lines_with_name(name_to_delete), 0)

    def _nb_lines_with_name(self, line_name):
        lines_with_name = self._lines_with_name(line_name)
        return len(lines_with_name)

    def _lines_with_name(self, name_filter):
        lines = self._xivo_ws.lines.list()
        lines_with_name = [line for line in lines if line.name == name_filter]
        return lines_with_name

    def test_edit_sip(self):
        line_id = self._init_sip_line({u'name': u'name_test_ws_edit_sip'})
        edited_line_attributes = {u'name': u'name_test_ws_edit_sip_edited',
                                  u'protocol': u'sip'}
        self._remove_lines(edited_line_attributes)
        ws_query = self._prepare_query_sip_line(edited_line_attributes)
        response = self._aws.edit(ws_query, line_id)

        self.assertEqual(response.code, 200)
        self._assert_only_one_line_with(edited_line_attributes)

    def test_delete_sip(self):
        line_id = self._init_sip_line({u'name': u'name_test_ws_remove_sip'})

        response = self._aws.delete(line_id)

        self.assertEqual(response.code, 200)
        self._assert_no_lines_with({u'name': u'name_test_ws_remove_sip',
                                    u'protocol': u'sip'})

    def test_add_custom(self):
        new_line_attributes = {u'interface': u'dahdi/g1',
                               u'protocol': u'custom'}
        self._remove_lines(new_line_attributes)
        ws_query = self._prepare_query_custom_line(new_line_attributes)

        response = self._aws.add(ws_query)

        self.assertEqual(response.code, 200)
        self._assert_only_one_line_with(new_line_attributes)

    def test_edit_custom(self):
        line_id = self._init_custom_line({u'interface': u'dahdi/g21'})
        edited_line_attributes = {u'interface': u'dahdi/g22',
                                  u'protocol': u'custom'}
        self._remove_lines(edited_line_attributes)
        ws_query = self._prepare_query_custom_line(edited_line_attributes)

        response = self._aws.edit(ws_query, line_id)

        self.assertEqual(response.code, 200)
        self._assert_only_one_line_with(edited_line_attributes)

    def test_delete_custom(self):
        line_id = self._init_custom_line({u'interface': u'dahdi/g3'})

        response = self._aws.delete(line_id)

        self.assertEqual(response.code, 200)
        self._assert_no_lines_with({u'interface': 'dahdi/g3',
                                    u'protocol': u'custom'})


    def _init_sip_line(self, line_attributes):
        self._remove_lines(line_attributes)
        return self._add_sip_line(line_attributes)

    def _init_custom_line(self, line_attributes):
        self._remove_lines(line_attributes)
        return self._add_custom_line(line_attributes)

    def _add_sip_line(self, line_attributes):
        ws_query = self._prepare_query_sip_line(line_attributes)
        self._aws.add(ws_query)
        lines = self._get_lines(line_attributes)
        return lines[0]['id']

    def _add_custom_line(self, line_attributes):
        ws_query = self._prepare_query_custom_line(line_attributes)
        self._aws.add(ws_query)
        lines = self._get_lines(line_attributes)
        return lines[0]['id']

    def _remove_lines(self, line_filter):
        sip_lines_to_remove = self._get_lines(line_filter)
        for sip_line in sip_lines_to_remove:
            self._aws.delete(sip_line['id'])

    def _prepare_query_sip_line(self, sip_line_properties):
        json_file_content = self._aws.get_json_file_content('linesip')
        return self._prepare_query(json_file_content, sip_line_properties)

    def _prepare_query_custom_line(self, custom_line_properties):
        json_file_content = self._aws.get_json_file_content('linecustom')
        return self._prepare_query(json_file_content, custom_line_properties)

    def _prepare_query(self, json_file_content, line_properties):
        jsonstr = json_file_content % (line_properties)
        return json.loads(jsonstr)

    def _assert_only_one_line_with(self, sip_line_filter):
        sip_lines_filtered = self._get_lines(sip_line_filter)
        self.assertEqual(len(sip_lines_filtered), 1)

    def _assert_no_lines_with(self, sip_line_filter):
        sip_lines_filtered = self._get_lines(sip_line_filter)
        self.assertEqual(len(sip_lines_filtered), 0)

    def _get_lines(self, line_filter):
        response = self._aws.list()
        if response.code == 204:
            return []
        else:
            lines = json.loads(response.data)
            lines_filtered = self._filter_lines(lines, line_filter)
            return lines_filtered

    def _filter_lines(self, lines, lines_filter):
        return [line for line in lines if self._match_line(line, lines_filter)]

    def _match_line(self, line, line_filter):
        try:
            for line_property in line_filter:
                if line[line_property] != line_filter[line_property]:
                    return False
            return True
        except KeyError:
            return False

if __name__ == '__main__':
    unittest.main()
