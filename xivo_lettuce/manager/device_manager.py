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

import os

from xivo_lettuce.common import open_url, remove_line
from xivo_lettuce import form
from selenium.common.exceptions import NoSuchElementException


def add_or_replace_device(info):
    delete_device(info)
    add_device(info)


def add_device(info):
    if 'mac' not in info:
        info['mac'] = _new_random_mac()
    open_url('device', 'add')
    form.input.edit_text_field_with_id('it-devicefeatures-mac', info['mac'])
    if 'ip' in info:
        form.input.edit_text_field_with_id('it-devicefeatures-ip', info['ip'])
    if 'protocol' in info:
        form.select.set_select_field_with_id('it-config-protocol', info['protocol'].upper())
    form.submit.submit_form()

    return info['mac']


def delete_device(info):
    search_device(info['mac'])
    try:
        remove_line(info['mac'])
    except NoSuchElementException:
        pass


def search_device(search):
    open_url('device')
    form.input.edit_text_field_with_id('it-toolbar-search', search)
    form.submit.submit_form('it-toolbar-subsearch')


def _new_random_mac():
    return ':'.join('%02x' % ord(c) for c in os.urandom(6))
