# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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


class PhoneRegister(object):

    def __init__(self):
        self._sip_phones = {}

    def add_registered_phone(self, phone, name):
        self._sip_phones[name] = phone

    def clear(self):
        for name in self._sip_phones.keys():
            del self._sip_phones[name]

    def get_user_phone(self, name):
        return self._sip_phones.get(name)
