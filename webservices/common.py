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

import json
from webservices import WebServices


class WSCommon(object):
    def __init__(self, module):
        self._aws = WebServices(module)

    def get_json_file_content(self, file):
        return self._aws.get_json_file_content(file)

    def list(self):
        response = self._aws.list()
        if response.data:
            return json.loads(response.data)
        return None

    def search(self, search):
        response = self._aws.search(search)
        if response.data:
            return json.loads(response.data)
        return None

    def view(self, id):
        response = self._aws.view(id)
        if not response:
            return None
        if response.data:
            return json.loads(response.data)
        return None

    def clear(self):
        response = self._aws.deleteall()
        if response.code == 200:
            return True
        return False

    def custom(self, qry={}, data=None):
        response = self._aws.custom(qry, data)
        if response.code == 200:
            return True
        return False

    def simple_add(self, content):
        response = self._aws.add(content)
        return (response.code == 200)

    def add(self, content):
        response = self._aws.add(content)
        if response.code == 200:
            response = self._aws.list()
            if response.code == 200:
                res = json.loads(response.data)
                if len(res) == 1 and 'id' in res[0]:
                    return res[0]['id']
        return False

    def edit(self, id, content):
        response = self._aws.edit(content, id)
        if response.code == 200:
            return True
        return False

    def delete(self, id):
        response = self._aws.delete(id)
        if response.code == 200:
            response = self._aws.list()
            if response.code == 204:
                return True
        return False

