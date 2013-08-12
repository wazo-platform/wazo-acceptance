# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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


def extract_webi_table_to_dict(table):
    list_tr = table.find_elements_by_tag_name('tr')

    headers_line = list_tr.pop(0)
    headers = _extract_th_from_tr_element(headers_line)

    lines = list()
    for tr_element in list_tr:
        td_elements = tr_element.find_elements_by_tag_name('td')
        td_elements_text = [td_element.text.strip() for td_element in td_elements]
        if len(td_elements_text) > 1:
            line_dict = dict(zip(headers, td_elements_text))
            lines.append(line_dict)

    return lines


def _extract_td_from_tr_elements(list_tr, headers, expected_headers):
    lines = list()
    for tr_element in list_tr:
        td_elements = tr_element.find_elements_by_tag_name('td')
        td_elements_text = [td_element.text.strip() for td_element in td_elements]
        line_dict = dict(zip(headers, td_elements_text))
        lines.append(line_dict)
    return lines


def _extract_th_from_tr_element(tr_element):
    header_th = tr_element.find_elements_by_tag_name('th')
    return [header.text.strip() for header in header_th]
