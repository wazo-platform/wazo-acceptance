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

import xivo_ws
import ConfigParser
import os

_CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '../../config/config.ini'))


def _open_config_file():
    local_config = '%s.local' % _CONFIG_FILE
    try:
        return open(local_config)
    except IOError:
        return open(_CONFIG_FILE)


config = ConfigParser.RawConfigParser()
with _open_config_file() as fobj:
    config.readfp(fobj)
hostname = config.get('xivo', 'hostname')
username = config.get('webservices_infos', 'login')
password = config.get('webservices_infos', 'password')

xivo_server_ws = xivo_ws.XivoServer(hostname, username, password)


def delete_with_id(obj, id_to_delete):
    obj_ws = getattr(xivo_server_ws, obj)
    for element in find_with_id(obj, id_to_delete):
        obj_ws.delete(element.id)


def delete_with_name(obj, name_to_delete):
    obj_ws = getattr(xivo_server_ws, obj)
    for element in find_with_name(obj, name_to_delete):
        obj_ws.delete(element.id)


def delete_with_number(obj, number_to_delete):
    obj_ws = getattr(xivo_server_ws, obj)
    for element in find_with_number(obj, number_to_delete):
        obj_ws.delete(element.id)


def delete_with_firstname_lastname(obj, firstname, lastname):
    obj_ws = getattr(xivo_server_ws, obj)
    for element in find_with_firstname_lastname(obj, firstname, lastname):
        obj_ws.delete(element.id)


def nb_with_name(obj, name):
    elements_with_name = find_with_name(obj, name)
    return len(elements_with_name)


def nb_with_number(obj, number):
    elements_with_number = find_with_number(obj, number)
    return len(elements_with_number)


def nb_with_firstname_lastname(obj, firstname, lastname):
    elements_with_name = find_with_firstname_lastname(obj, firstname, lastname)
    return len(elements_with_name)


def find_with_id(obj, id_to_find):
    obj_ws = getattr(xivo_server_ws, obj)
    list = obj_ws.list()
    return [element for element in list if element.id == id_to_find]


def find_with_name(obj, name_filter):
    obj_ws = getattr(xivo_server_ws, obj)
    list = obj_ws.list()
    return [element for element in list if element.name == name_filter]


def find_with_number(obj, number_filter):
    obj_ws = getattr(xivo_server_ws, obj)
    list = obj_ws.list()
    return [element for element in list if element.number == number_filter]


def find_with_firstname_lastname(obj, firstname, lastname):
    obj_ws = getattr(xivo_server_ws, obj)
    list = obj_ws.search('%s %s' % (firstname, lastname))
    return [element for element in list if
            element.firstname == firstname and
            element.lastname == lastname]
