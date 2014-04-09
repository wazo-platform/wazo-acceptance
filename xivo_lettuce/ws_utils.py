# -*- coding: utf-8 -*-

# Copyright (C) 2012-2014 Avencall
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

from hamcrest import assert_that, has_key
import requests
import json

DEFAULT_CONTENT_TYPE = 'application/json'


class WsUtils(object):
    '''
    This helper class is a forerunner of a library
    proposing methods for easy implementation of
    REST web services
    '''

    def __init__(self, rest_configuration_obj):
        self.baseurl = self._prepare_baseurl(rest_configuration_obj)
        self.auth = self._prepare_auth(rest_configuration_obj)
        self.headers = self._prepare_headers(rest_configuration_obj)
        self.session = requests.Session()

    def _prepare_baseurl(self, rest_configuration_obj):
        protocol = rest_configuration_obj.protocol
        hostname = rest_configuration_obj.hostname
        port = rest_configuration_obj.port

        baseurl = "%s://%s:%s" % (protocol, hostname, port)

        api_version = rest_configuration_obj.api_version
        if api_version is not None:
            baseurl = '%s/%s' % (baseurl, api_version)

        return baseurl

    def _prepare_auth(self, rest_configuration_obj):
        username = rest_configuration_obj.auth_username
        password = rest_configuration_obj.auth_passwd

        if username is None and password is None:
            return None

        auth = requests.auth.HTTPDigestAuth(username, password)
        return auth

    def _prepare_headers(self, rest_configuration_obj):
        headers = {}
        headers.update({'Content-Type': rest_configuration_obj.content_type})
        return headers

    def rest_get(self, path, **kwargs):
        request = self._prepare_request('GET', path, **kwargs)
        return self._process_request(request)

    def rest_post(self, path, payload, **kwargs):
        data = json.dumps(payload)
        request = self._prepare_request('POST', path, data=data, **kwargs)
        return self._process_request(request)

    def rest_put(self, path, payload, **kwargs):
        data = json.dumps(payload)
        request = self._prepare_request('PUT', path, data=data, **kwargs)
        return self._process_request(request)

    def rest_delete(self, path, **kwargs):
        request = self._prepare_request('DELETE', path, **kwargs)
        return self._process_request(request)

    def _prepare_request(self, method, path, **kwargs):
        if not path.startswith('/'):
            path = '/%s' % path
        url = "%s%s" % (self.baseurl, path)

        return requests.Request(method=method,
                                url=url,
                                headers=self.headers,
                                auth=self.auth,
                                **kwargs)

    def _process_request(self, request):
        prep = request.prepare()
        response = self.session.send(prep, verify=False, allow_redirects=False)
        return self._process_response(response)

    def _process_response(self, response):
        status_code = response.status_code
        body = response.text
        headers = response.headers

        try:
            body = json.loads(body)
        except:
            pass

        return RestResponse(response.url, status_code, headers, body)


class RestResponse(object):

    def __init__(self, url, status, headers, data):
        self.url = url
        self.status = status
        self.headers = headers
        self.data = data

    def items(self):
        self.check_status()
        assert_that(self.data, has_key('items'))
        return self.data['items']

    def status_ok(self):
        return self.status in (200, 201, 204)

    def resource(self):
        self.check_status()
        return self.data

    def check_status(self):
        assert_that(self.status_ok(), self.data)


class RestConfiguration(object):

    def __init__(self, protocol, hostname, port, auth_username=None, auth_passwd=None,
                 api_version=None, content_type=DEFAULT_CONTENT_TYPE):
        self.protocol = protocol
        self.hostname = hostname
        self.port = port
        self.auth_username = auth_username
        self.auth_passwd = auth_passwd
        self.api_version = api_version
        self.content_type = content_type
