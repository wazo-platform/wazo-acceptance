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

from xivo_lettuce.sccppy.msg.msg import Msg, RegisterMsg, Uint32


class TestUint32(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.FooMsg = Msg(0, Uint32('foo'))

    def setUp(self):
        self.foo_msg = self.FooMsg()

    def test_default_value(self):
        self.assertEqual(0, self.foo_msg.foo)

    def test_set_valid_value(self):
        self.foo_msg.foo = 42

        self.assertEqual(42, self.foo_msg.foo)

    def test_set_invalid_values(self):
        values = [-1, 2 ** 32, 3.1416]
        for value in values:
            try:
                self.foo_msg.foo = value
            except ValueError:
                pass
            except Exception:
                self.fail('setting value %s should raise a ValueError' % value)


class TestMsg(unittest.TestCase):

    def test_register_msg(self):
        register_msg = RegisterMsg()

        self.assertEqual(register_msg.name, '')
        self.assertEqual(register_msg.user_id, 0)
        self.assertEqual(register_msg.proto_version, 0)

        register_msg.name = 'SEP007'
        register_msg.user_id = 42
        register_msg.proto_version = 42

        self.assertEqual(register_msg.name, 'SEP007')
        self.assertEqual(register_msg.user_id, 42)
        self.assertEqual(register_msg.proto_version, 42)
