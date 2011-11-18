# -*- coding: utf-8 -*-

__license__ = """
    Copyright (C) 2011 Avencall

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

import pprint
import json
import os
import urllib
import urllib2

JSON_DIR = os.path.join(os.path.dirname(__file__), '../xivojson')
URI = 'https://skaro-daily.lan-quebec.avencall.com:443'
USERNAME = 'admin'
PASSWORD = 'proformatique'

class WebServices(object):
    def __init__(self, wsobj, uri_prefix=URI, username=USERNAME, password=PASSWORD):
        self.wsobj = wsobj
        self.basepath = os.path.normpath(JSON_DIR)
        self._path = self._compute_path(uri_prefix)
        self._uri_prefix = uri_prefix
        self._opener = self._build_opener(uri_prefix, username, password)
        self._headers = {
            "Content-type": "application/json",
            "Accept": "text/plain"
        }

    def get_uri(self):
        list = {
                "users"  : "/service/ipbx/json.php/%s/pbx_settings/users",
                "groups" : "/service/ipbx/json.php/%s/pbx_settings/groups"
               }
        uri = [list[self.wsobj] for uri in list
                if uri == self.wsobj]
        if len(uri) > 0:
            return uri[0]
        else:
            raise 'uri not exist for object %s' % self.wsobj

    def _compute_path(self, uri_prefix):
        if 'localhost' in uri_prefix or '127.0.0.1' in uri_prefix:
            method = 'private'
        else:
            method = 'restricted'
        return self.get_uri() % method

    def _build_opener(self, uri_prefix, username, password):
        handlers = []
        if username is not None or password is not None:
            pwd_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
            pwd_manager.add_password(None, uri_prefix, username, password)
            handlers.append(urllib2.HTTPBasicAuthHandler(pwd_manager))
        return urllib2.build_opener(*handlers)

    def _build_query(self, qry):
        return urllib.urlencode(qry)

    def _request_http(self, qry, data=None):
        if data is not None:
            if isinstance(data, dict):
                data = json.dumps(data)
            data = data.replace(' ', '').replace('\n', '')
        url = '%s%s?%s' % (self._uri_prefix, self._path, self._build_query(qry))
        request = urllib2.Request(url=url, data=data, headers=self._headers)
        self._handle = self._opener.open(request)
        return self._handle

    def get_last_request_status(self):
        if hasattr(self._handle, 'code'):
            return self._handle.code, self._handle.msg

    def list(self):
        qry = {"act": "list"}
        fobj = self._request_http(qry)
        return fobj.code, fobj.readline()

    def add(self, content):
        qry = {"act": "add"}
        fobj = self._request_http(qry, content)
        return fobj.code, fobj.readline()

    def edit(self, content, id):
        qry = {"act": "edit", "id": id}
        fobj = self._request_http(qry, content)
        return fobj.code, fobj.readline()

    def view(self, id):
        qry = {"act": "view", "id": id}
        fobj = self._request_http(qry)
        return fobj.code, fobj.readline()

    def search(self, search):
        qry = {"act": "search", "search": search}
        fobj = self._request_http(qry)
        return fobj.code, fobj.readline()

    def delete(self, id):
        qry = {"act": "delete", "id": id}
        fobj = self._request_http(qry)
        return fobj.code, fobj.readline()

    def deleteall(self):
        qry = {"act": "deleteall"}
        fobj = self._request_http(qry)
        return fobj.code, fobj.readline()

