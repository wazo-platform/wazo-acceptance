# -*- coding: utf-8 -*-

# Copyright (C) 2013  Avencall
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

    _PATH = 'service/ipbx/web_services.php/phonebook/search/'
    _HEADERS = {'User-Agent': 'Aastra6731i MAC:00-08-5D-31-EF-D2 V:3.2.2.1136-SIP'}
    _REGEX = re.compile(r'<Prompt><!\[CDATA\[(.+?)\]\]></Prompt>')

    def search(self, name):
        request = self._new_request(name)
        fobj = urllib2.urlopen(request)
        try:
            return self._parse_response(fobj)
        finally:
            fobj.close()

    def _new_request(self, name):
        url = '%s%s?name=%s' % (world.host, self._PATH, name)
        return urllib2.Request(url, headers=self._HEADERS)

    def _parse_response(self, fobj):
        results = []
        for line in fobj:
            m = self._REGEX.match(line)
            if m:
                results.append(m.group(1))
        return results
