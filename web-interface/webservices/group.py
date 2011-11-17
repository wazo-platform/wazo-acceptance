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
import cjson
from xivojson import *

class WsGroup(object):
    def __init__(self):
        global IP, PORT, SSL, USERNAME, PASSWORD
        self.client = JSONClient(IP, PORT, SSL, USERNAME, PASSWORD)
        self.obj    = 'groups'

    def list(self):
        (resp, data) = self.client.list(self.obj)
        #pprint.pprint(data)
        res = json.loads(data)
        return res

    def add(self, data):
        (resp, data) = self.client.add(self.obj, data)
        return (resp.status == 200)
    
    def search(self, search):
        (resp, data) = self.client.search(self.obj, search)
        res = json.loads(data)
        return res

    def view(self, id):
        (resp, data) = self.client.view(self.obj, id)
        res = json.loads(data)
        return res

    def delete(self, id):
        (resp, data) = self.client.delete(self.obj, id)
        return (resp.status == 200)

    def clear(self):
        (resp, data) = self.client.deleteall(self.obj)
        return (resp.status == 200)

if __name__ == '__main__':
    pass