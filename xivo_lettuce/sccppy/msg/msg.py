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

import struct


def Msg(msg_id, *fields):
    fields_by_name = dict((field.name, field) for field in fields)
    if len(fields) != len(fields_by_name):
        raise Exception('same field name used twice')

    class_dict = {
        'MSG_ID': msg_id,
        '_FIELDS': fields,
    }
    class_dict.update(fields_by_name)

    return type('Msg0x%04X' % msg_id, (_BaseMsg,), class_dict)


class _BaseMsg(object):

    def serialize(self):
        # TODO
        pass

    def deserialize(self, buf):
        # TODO
        pass


class _BaseField(object):

    def __init__(self, name, value_class):
        # TODO rename value_class
        self.name = name
        self._obj_name = '_fieldval_%s' % name
        self._value_class = value_class

    def __get__(self, obj, objtype):
        return getattr(obj, self._obj_name, self._value_class.default)

    def __set__(self, obj, value):
        self._value_class.check_value(value)
        setattr(obj, self._obj_name, value)

    def serialize(self, obj, fobj):
        value = getattr(obj, self._obj_name, self._value_class.default)
        return self._value_class.serialize_value(value, fobj)


class _Uint32(object):

    # TODO rename stuff
    _MINVAL = 0
    _MAXVAL = 2 ** 32 - 1
    _FORMAT = struct.Struct('<L')

    default = 0

    def check_value(self, value):
        if not isinstance(value, int):
            raise ValueError('expected integer type; got %s type' % type(value).__name__)
        if not self._MINVAL <= value <= self._MAXVAL:
            raise ValueError('value %s is out of range' % value)

    def serialize_value(self, value, fobj):
        fobj.write(self._FORMAT.pack(value))

    def deserialize_value(self, fobj):
        return self._FORMAT.unpack(fobj.read(4))[0]


def Uint32(name):
    return _BaseField(name, _Uint32())


class _Uint8(object):

    # TODO rename stuff
    _MINVAL = 0
    _MAXVAL = 2 ** 8 - 1

    default = 0

    def check_value(self, value):
        if not isinstance(value, int):
            raise ValueError('expected integer type; got %s type' % type(value).__name__)
        if not self._MINVAL <= value <= self._MAXVAL:
            raise ValueError('value %s is out of range' % value)


def Uint8(name):
    return _BaseField(name, _Uint8())


class _Bytes(object):

    default = ''

    def __init__(self, length):
        self._length = length

    def check_value(self, value):
        # str instead of basestring since unicode is not valid
        if not isinstance(value, str):
            raise ValueError('expected str type; got %s type' % type(value).__name__)
        if len(value) > self._length:
            raise ValueError('value %s is too long' % value)


def Bytes(name, length):
    return _BaseField(name, _Bytes(length))


REGISTER_MSG_ID = 0x0001


RegisterMsg = Msg(REGISTER_MSG_ID,
    Bytes('name', 16),
    Uint32('user_id'),
    Uint32('line_instance'),
    Uint32('ip'),
    Uint32('type'),
    Uint32('max_streams'),
    Uint32('active_streams'),
    Uint8('proto_version'),
)
