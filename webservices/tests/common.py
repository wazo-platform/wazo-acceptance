# -*- coding: utf-8 -*-
# Copyright (C) 2012-2016 Avencall
# SPDX-License-Identifier: GPL-3.0+

import os

import xivo_ws


XIVO_HOST = os.environ.get('XIVO_HOST', 'daily-xivo-pxe.lan.proformatique.com')
XIVO_CONFD_PORT = os.environ.get('XIVO_CONFD_PORT', 9486)
XIVO_CONFD_USERNAME = os.environ.get('XIVO_CONFD_USERNAME', 'admin')
XIVO_CONFD_PASSWORD = os.environ.get('XIVO_CONFD_PASSWORD', 'proformatique')


xivo_server_ws = xivo_ws.XivoServer(host=XIVO_HOST,
                                    username=XIVO_CONFD_USERNAME,
                                    password=XIVO_CONFD_PASSWORD)


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
