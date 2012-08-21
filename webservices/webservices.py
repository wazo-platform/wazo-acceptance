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
import urllib
import urllib2
import ConfigParser

JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'xivojson'))
_CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '../config/config.ini'))

URILIST = {'ipbx': {
                'call_management':
                {
                    "incall": "/service/ipbx/json.php/%s/call_management/incall",
                    "outcall": "/service/ipbx/json.php/%s/call_management/outcall",
                    "pickup": "/service/ipbx/json.php/%s/call_management/pickup"
                },
                'control_system':
                {
                    "reload": "/service/ipbx/json.php/%s/control_system/reload",
                    "restart": "/service/ipbx/json.php/%s/control_system/restart"
                },
                'general_settings':
                {
                    "advanced": "/service/ipbx/json.php/%s/general_settings/advanced",
                    "iax": "/service/ipbx/json.php/%s/general_settings/iax",
                    "outboundmwi": "/service/ipbx/json.php/%s/general_settings/outboundmwi",
                    "phonebook": "/service/ipbx/json.php/%s/general_settings/phonebook",
                    "sip": "/service/ipbx/json.php/%s/general_settings/sip",
                    "voicemail": "/service/ipbx/json.php/%s/general_settings/voicemail"
                },
                'pbx_services':
                {
                    "extenfeatures": "/service/ipbx/json.php/%s/pbx_services/extenfeatures",
                    "phonebook": "/service/ipbx/json.php/%s/pbx_services/phonebook"
                },
                'pbx_settings':
                {
                    "groups": "/service/ipbx/json.php/%s/pbx_settings/groups",
                    "lines": "/service/ipbx/json.php/%s/pbx_settings/lines",
                    "meetme": "/service/ipbx/json.php/%s/pbx_settings/meetme",
                    "users": "/service/ipbx/json.php/%s/pbx_settings/users",
                    "voicemail": "/service/ipbx/json.php/%s/pbx_settings/voicemail"
                },
                'phonebook':
                {
                    "local": "/service/ipbx/json.php/%s/pbx_settings/local",
                    "menu": "/service/ipbx/json.php/%s/pbx_settings/menu",
                    "search": "/service/ipbx/json.php/%s/pbx_settings/search"
                 },
                'system_management':
                {
                    "context": "/service/ipbx/json.php/%s/system_management/context"
                },
                'trunk_management':
                {
                    "sip": "/service/ipbx/json.php/%s/trunk_management/sip",
                    "iax": "/service/ipbx/json.php/%s/trunk_management/iax",
                    "custom": "/service/ipbx/json.php/%s/trunk_management/custom"
                }
            },
            'callcenter':
            {
                'settings':
                {
                    "agents": "/callcenter/json.php/%s/settings/agents/",
                    "queues": "/callcenter/json.php/%s/settings/queues/",
                    "skills": "/callcenter/json.php/%s/settings/queueskills/",
                    "queueskillrules": "/callcenter/json.php/%s/settings/queueskillrules/"
                }
            },
            'configuration':
            {
                'manage':
                {
                    "entity": "/xivo/configuration/json.php/%s/manage/entity"
                },
                'network':
                {
                    "dhcp": "/xivo/configuration/json.php/%s/network/dhcp",
                    "mail": "/xivo/configuration/json.php/%s/network/mail",
                    "interface": "/xivo/configuration/json.php/%s/network/interface",
                    "resolvconf": "/xivo/configuration/json.php/%s/network/resolvconf"
                },
                'provisioning':
                {
                    "general": "/xivo/configuration/json.php/%s/provisioning/general"
                },
                'support':
                {
                    "monitoring": "/xivo/configuration/json.php/%s/support/monitoring"
                },
                'check': "/xivo/configuration/json.php/%s/check"
            }
       }


class WebServices(object):
    def __init__(self, module, uri_prefix=None, username=None, password=None):
        config = ConfigParser.RawConfigParser()
        with self._open_config_file() as fobj:
            config.readfp(fobj)
        if not uri_prefix:
            uri_prefix = 'https://%s:443' % config.get('xivo', 'hostname')
        if not username:
            username = config.get('webservices_infos', 'login')
        if not password:
            password = config.get('webservices_infos', 'password')

        self.basepath = os.path.normpath(JSON_DIR)
        self.module = module
        self._wsr = None
        self._path = self._compute_path(uri_prefix)
        self._uri_prefix = uri_prefix
        self._headers = {"Content-type": "application/json",
                         "Accept": "text/plain"}
        self._add_authentication_header(username, password)

    def _add_authentication_header(self, username, password):
        if username is not None and username != '':
            import base64
            base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
            self._headers["Authorization"] = "Basic %s" % base64string

    def _open_config_file(self):
        local_config = '%s.local' % _CONFIG_FILE
        try:
            return open(local_config)
        except IOError:
            return open(_CONFIG_FILE)

    def _compute_path(self, uri_prefix):
        if 'localhost' in uri_prefix or '127.0.0.1' in uri_prefix:
            method = 'private'
        else:
            method = 'restricted'
        return self._get_uri_format_string() % method

    def _get_uri_format_string(self):
        sections = self.module.split('/')
        tmp = URILIST
        for section in sections:
            if section in tmp:
                tmp = tmp[section]

        if isinstance(tmp, basestring):
            return tmp
        else:
            raise Exception("URI doesn't exist for module %r" % self.module)

    def get_json_file_content(self, file):
        filename = '%s.json' % file
        abs_file_path = os.path.join(self.basepath, filename)
        with open(abs_file_path) as fobj:
            jsonfilecontent = fobj.read()
        return jsonfilecontent

    def _request_http(self, qry, data=None):
        if isinstance(data, dict):
            data = json.dumps(data)
        url = '%s%s?%s' % (self._uri_prefix, self._path, self._build_query(qry))
        request = urllib2.Request(url=url, data=data, headers=self._headers)
        try:
            handle = urllib2.urlopen(request)
            self._wsr = WebServicesResponse(url, handle.code, handle.read())
            handle.close()
        except urllib2.HTTPError, e:
            self._wsr = WebServicesResponse(url, e.code, None)
        return self._wsr

    def _build_query(self, qry):
        return urllib.urlencode(qry)

    def get_last_response(self):
        return self._wsr

    def call(self):
        return self._request_http({})

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

    def custom(self, qry, content=None):
        return self._request_http(qry, content)


class WebServicesResponse(object):
    def __init__(self, url, code, data):
        self.url = url
        self.code = code
        self.data = data


class WebServicesFactory(object):
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

    def add(self, data):
        response = self._aws.add(data)
        return (response.code == 200)

    def edit(self, id, data):
        response = self._aws.edit(data, id)
        return (response.code == 200)

    def delete(self, id):
        response = self._aws.delete(id)
        if not response:
            return False
        return (response.code == 200)

    def clear(self):
        response = self._aws.deleteall()
        return (response.code == 200)

    def custom(self, qry={}, data=None):
        return self._aws.custom(qry, data)
