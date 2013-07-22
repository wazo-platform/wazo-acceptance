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

import unittest

from xivo_lettuce.sccppy.msg.base import Msg, \
    _Uint32FieldType, _Uint8FieldType, _BytesFieldType, Uint32


class BaseTestFieldType(object):

    def test_default_value(self):
        self.assertEqual(self.default_value, self.field_type.default)

    def test_check_valid_value(self):
        for value in self.valid_values:
            self.field_type.check(value)

    def test_check_invalid_values(self):
        for value in self.invalid_values:
            self.assertRaises(ValueError, self.field_type.check, value)

    def test_serialize(self):
        for value, expected_string in self.serialize_test_table:
            string = self.field_type.serialize(value)

            self.assertEqual(expected_string, string)

    def test_deserialize(self):
        for expected_value, string in self.serialize_test_table:
            value = self.field_type.deserialize(string)

            self.assertEqual(expected_value, value)


class TestUint32(BaseTestFieldType, unittest.TestCase):

    field_type = _Uint32FieldType()

    default_value = 0
    valid_values = [0, 42, 2 ** 32 - 1]
    invalid_values = [-1, 2 ** 32, 3.14]

    serialize_test_table = [
        (0x1122, '\x22\x11\x00\x00'),
    ]


class TestUint8(BaseTestFieldType, unittest.TestCase):

    field_type = _Uint8FieldType()

    default_value = 0
    valid_values = [0, 42, 2 ** 8 - 1]
    invalid_values = [-1, 2 ** 8, 3.14]

    serialize_test_table = [
        (0x11, '\x11'),
    ]


class TestBytes(BaseTestFieldType, unittest.TestCase):

    field_type = _BytesFieldType(4)

    default_value = ''
    valid_values = ['', 'abcd']
    invalid_values = ['abcde', 1, 3.14]

    serialize_test_table = [
        ('abcd', 'abcd'),
        ('ab', 'ab\x00\x00'),
        ('', '\x00\x00\x00\x00'),
    ]


class TestMsg(unittest.TestCase):

    msg_id = 42
    field = Uint32('foo')

    FakeMsg = Msg(msg_id, field)

    def setUp(self):
        self.msg = self.FakeMsg()

    def test_msg_id(self):
        self.assertEqual(self.msg_id, self.FakeMsg.id)
        self.assertEqual(self.msg_id, self.msg.id)

    def test_msg_default_value(self):
        self.assertEqual(0, self.msg.foo)

    def test_msg_set_value(self):
        self.msg.foo = 42

        self.assertEqual(42, self.msg.foo)

    def test_serialize(self):
        self.msg.foo = 0x1122

        string = self.msg.serialize()

        self.assertEqual('\x22\x11\x00\x00', string)

    def test_deserialize(self):
        self.msg.deserialize('\x22\x11\x00\x00')

        self.assertEqual(0x1122, self.msg.foo)
