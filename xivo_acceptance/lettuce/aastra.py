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
import requests
import string
from lettuce import world


class AastraPhonebookBrowser(object):

    # TODO change this, this is actually for Cisco
    _REGEX_DISPLAY = re.compile(r'<Name>(.+)</Name>')
    _REGEX_NUMBER = re.compile(r'<Telephone>(.+)</Telephone>')

    def __init__(self, mac_address):
        user_agent = 'Aastra6731i MAC:{} V:3.2.2.1136-SIP'.format(mac_address.replace(':', '-'))
        self._session = requests.Session()
        self._session.headers = {'User-Agent': user_agent}
        input_url = self._get_phonebook_input_url(mac_address)
        self._lookup_url = self._get_phonebook_lookup_url(input_url)

    def _get_phonebook_input_url(self, mac_address):
        filename = ''.join(c for c in mac_address if c in string.hexdigits)
        url = 'http://{}:8667/Aastra/{}.cfg'.format(world.config['xivo_host'], filename)
        r = self._session.get(url)
        if r.status_code != 200:
            r.raise_for_status()

        regex = re.compile(r'prgkey8 value: (http.+)$')
        for line in r.content.splitlines():
            m = regex.match(line)
            if m:
                return m.group(1)
        raise Exception('could not extract input URL')

    def _get_phonebook_lookup_url(self, input_url):
        r = self._session.get(input_url)
        if r.status_code != 200:
            r.raise_for_status()

        # TODO change this, this is actually for Cisco
        regex = re.compile(r'<URL>(.+)</URL>')
        for line in r.content.splitlines():
            m = regex.search(line)
            if m:
                return m.group(1)
        raise Exception('could not extract lookup URL')

    def search(self, term):
        url = '{}&term={}'.format(self._lookup_url, term.encode('utf-8'))
        r = self._session.get(url)
        if r.status_code != 200:
            r.raise_for_status()

        return self._parse_response(r.content)

    def _parse_response(self, content):
        lines = content.splitlines()
        names = self._accumulate_display(lines)
        numbers = self._accumulate_number(lines)
        return [{'name': name, 'number': number} for name, number in zip(names, numbers)]

    def _accumulate_display(self, lines):
        return self._accumulate_result(lines, self._REGEX_DISPLAY)

    def _accumulate_number(self, lines):
        return self._accumulate_result(lines, self._REGEX_NUMBER)

    def _accumulate_result(self, lines, regex):
        results = []
        for line in lines:
            m = regex.search(line)
            if m:
                result = m.group(1).decode('utf8')
                results.append(result)
        return results
