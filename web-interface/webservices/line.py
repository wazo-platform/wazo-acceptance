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


class WsLine(object):
    def __init__(self):
        self._aws = WebServices(wsobj='lines')

    def list(self):
        (code, data) = self._aws.list()
        if data:
            data = json.loads(data)
        return data

    def add(self, data):
        (code, data) = self._aws.add(data)
        return (code == 200)

    def search(self, search):
        (code, data) = self._aws.search(search)
        res = json.loads(data)
        return res

    def view(self, id):
        (code, data) = self._aws.view(id)
        res = json.loads(data)
        return res

    def delete(self, id):
        (code, data) = self._aws.delete(id)
        return (code == 200)

    def clear(self):
        (code, data) = self._aws.deleteall()
        return (code == 200)
