# -*- coding: UTF-8 -*-

import unittest
from xivo_lettuce.sccppy.msg.msg import RegisterMsg


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
