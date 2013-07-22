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
        'id': msg_id,
        '_fields': fields,
    }
    class_dict.update(fields_by_name)

    return type('Msg0x%04X' % msg_id, (_BaseMsg,), class_dict)


class _BaseMsg(object):

    def serialize(self):
        return ''.join(field.field_type.serialize(getattr(self, field.name))
                       for field in self._fields)

    def deserialize(self, body):
        offset = 0
        for field in self._fields:
            size = field.field_type.size
            data = body[offset:offset + size]
            offset += size
            setattr(self, field.name, field.field_type.deserialize(data))


class _Field(object):

    def __init__(self, name, field_type):
        self.name = name
        self.field_type = field_type
        self._obj_name = '_fieldval_%s' % name

    def __get__(self, obj, objtype):
        return getattr(obj, self._obj_name, self.field_type.default)

    def __set__(self, obj, value):
        self.field_type.check(value)
        setattr(obj, self._obj_name, value)


class _Uint32FieldType(object):

    _MAXVAL = 2 ** 32 - 1
    _FORMAT = struct.Struct('<I')

    default = 0
    size = 4

    def check(self, value):
        if not isinstance(value, int):
            raise ValueError('expected integer type; got %s type' % type(value).__name__)
        if not 0 <= value <= self._MAXVAL:
            raise ValueError('value %s is out of range' % value)

    def serialize(self, value):
        return self._FORMAT.pack(value)

    def deserialize(self, data):
        return self._FORMAT.unpack(data)[0]


class _Uint8FieldType(object):

    _MAXVAL = 2 ** 8 - 1

    default = 0
    size = 1

    def check(self, value):
        if not isinstance(value, int):
            raise ValueError('expected integer type; got %s type' % type(value).__name__)
        if not 0 <= value <= self._MAXVAL:
            raise ValueError('value %s is out of range' % value)

    def serialize(self, value):
        return chr(value)

    def deserialize(self, data):
        return ord(data[0])


class _BytesFieldType(object):

    default = ''

    def __init__(self, size):
        self.size = size

    def check(self, value):
        # str instead of basestring since unicode is not valid
        if not isinstance(value, str):
            raise ValueError('expected str type; got %s type' % type(value).__name__)
        if len(value) > self.size:
            raise ValueError('value %s is too long' % value)

    def serialize(self, value):
        return value.ljust(self.size, '\x00')

    def deserialize(self, data):
        return data.rstrip('\x00')


def Uint32(name):
    return _Field(name, _Uint32FieldType())


def Uint8(name):
    return _Field(name, _Uint8FieldType())


def Bytes(name, length):
    return _Field(name, _BytesFieldType(length))
