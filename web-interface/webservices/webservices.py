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

import json
import os
import urllib2
import ConfigParser

JSON_DIR = os.path.join(os.path.dirname(__file__), '../xivojson')
CONFIG_FILE = os.path.join(os.path.dirname(__file__), '../config/config.ini')


class WebServices(object):
    def __init__(self, module, uri_prefix=None, username=None, password=None):
        
        _config = ConfigParser.RawConfigParser()
        with open(CONFIG_FILE) as fobj:
            _config.readfp(fobj)
        if not uri_prefix:
            uri_prefix = _config.get('webservices_infos', 'host')
        if not username:
            username = _config.get('webservices_infos', 'login')
        if not password:
            password = _config.get('webservices_infos', 'password')
        
        self.basepath = os.path.normpath(JSON_DIR)
        self.module = module
        self._wsr = None
        self._path = self._compute_path(uri_prefix)
        self._uri_prefix = uri_prefix
        self._opener = self._build_opener(uri_prefix, username, password)
        self._headers = {
                            "Content-type": "application/json",
                            "Accept": "text/plain"
                        }

    def get_json_file_content(self, file):
        filename = '%s.json' % file
        abs_file_path = os.path.join(self.basepath, filename);
        with open(abs_file_path) as fobj:
            jsonfilecontent = fobj.read()
        return jsonfilecontent

    def get_uri(self):
        list = {
                "users"  : "/service/ipbx/json.php/%s/pbx_settings/users",
                "groups" : "/service/ipbx/json.php/%s/pbx_settings/groups",
                "lines"  : "/service/ipbx/json.php/%s/pbx_settings/lines",
                "meetme" : "/service/ipbx/json.php/%s/pbx_settings/meetme",
                
                "incall" : "/service/ipbx/json.php/%s/call_management/incall",
                
                "context" : "/service/ipbx/json.php/%s/system_management/context",
                
                "trunksip" : "/service/ipbx/json.php/%s/trunk_management/sip",
                
                "agents" : "/callcenter/json.php/%s/settings/agents/",
                
                "entity" : "/xivo/configuration/json.php/%s/manage/entity",
                
                "dhcp" : "/xivo/configuration/json.php/%s/network/dhcp",
                "mail" : "/xivo/configuration/json.php/%s/network/mail",
                "monitoring" : "/xivo/configuration/json.php/%s/support/monitoring"
               }
        module = [self.module, '%ss' % self.module]
        for mod_exist in module:
            if mod_exist in list:
                return list[mod_exist]
        
        raise 'uri not exist for object %s' % self.module

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
        import urllib
        return urllib.urlencode(qry)

    def _request_http(self, qry, data=None):
        if data is not None:
            if isinstance(data, dict):
                data = json.dumps(data)
            data = data.replace(' ', '').replace('\n', '')
        url = '%s%s?%s' % (self._uri_prefix, self._path, self._build_query(qry))
        request = urllib2.Request(url=url, data=data, headers=self._headers)
        try:
            handle = self._opener.open(request)
            self._wsr = WebServicesResponse(url, handle.code, handle.read())
            handle.close()
        except urllib2.HTTPError, e:
            self._wsr = WebServicesResponse(url, e.code, e.read())
        return self._wsr

    def get_last_response(self):
        if self._wsr:
            return self._wsr

    def list(self):
        qry = {"act": "list"}
        return self._request_http(qry)

    def add(self, content):
        qry = {"act": "add"}
        return self._request_http(qry, content)

    def edit(self, content, id):
        qry = {"act": "edit", "id": id}
        return self._request_http(qry, content)

    def view(self, id):
        qry = {"act": "view", "id": id}
        return self._request_http(qry)

    def search(self, search):
        qry = {"act": "search", "search": search}
        return self._request_http(qry)

    def delete(self, id):
        qry = {"act": "delete", "id": id}
        return self._request_http(qry)

    def deleteall(self):
        qry = {"act": "deleteall"}
        return self._request_http(qry)


class WebServicesResponse(object):
    def __init__(self, url, code, data):
        self.url = url
        self.code = code
        self.data = data


class WebServicesFactory(object):
    def __init__(self, module):
        self._aws = WebServices(module=module)

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
        if response.data:
            return json.loads(response.data)
        return None

    def add(self, data):
        response = self._aws.add(data)
        return (response.code == 200)

    def edit(self, id, data):
        response = self._aws.view(id, data)
        return (response.code == 200)

    def delete(self, id):
        response = self._aws.delete(id)
        return (response.code == 200)

    def clear(self):
        response = self._aws.deleteall()
        return (response.code == 200)
