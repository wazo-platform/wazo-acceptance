# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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

import re
import urllib2
from lettuce import world


class AastraPhonebookBrowser(object):

    _PATH = '/service/ipbx/web_services.php/phonebook/search/'
    _HEADERS = {'User-Agent': 'Aastra6731i MAC:00-08-5D-31-EF-D2 V:3.2.2.1136-SIP'}
    _REGEX_DISPLAY = re.compile(r'<Prompt><!\[CDATA\[(.+?)\]\]></Prompt>')
    _REGEX_NUMBER = re.compile(r'<URI>Dial:<!\[CDATA\[(.+?)\]\]></URI>')

    def search(self, name):
        request = self._new_request(name)
        fobj = urllib2.urlopen(request)
        try:
            return self._parse_response(fobj)
        finally:
            fobj.close()

    def _parse_response(self, fobj):
        lines = fobj.readlines()
        names = self._accumulate_display(lines)
        numbers = self._accumulate_number(lines)
        return [{'name': name, 'number': number} for name, number in zip(names, numbers)]

    def _new_request(self, name):
        encoded_name = name.encode('utf8')
        url = '%s%s?name=%s' % (world.config['frontend']['url'], self._PATH, encoded_name)
        return urllib2.Request(url, headers=self._HEADERS)

    def _accumulate_display(self, lines):
        return self._accumulate_result(lines, self._REGEX_DISPLAY)

    def _accumulate_number(self, lines):
        return self._accumulate_result(lines, self._REGEX_NUMBER)

    def _accumulate_result(self, lines, regex):
        results = []
        for line in lines:
            m = regex.match(line)
            if m:
                result = m.group(1).decode('utf8')
                results.append(result)
        return results
