# -*- coding: UTF-8 -*-

import unittest
from loadtester import screen


NO_SESSION = """\
No Sockets found in /var/run/screen/S-trafgen.
"""

ONE_SESSION = """\
There is a screen on:
\t4569.pts-1.trafgen\t(11/11/11 09:47:26 AM)\t(Attached)
1 Socket in /var/run/screen/S-trafgen.
"""

TWO_SESSIONS = """\
There are screens on:
\t4569.pts-1.trafgen\t(11/11/11 09:47:26 AM)\t(Attached)
\t4741.loadtester-call-and-wait\t(11/11/11 09:54:26 AM)\t(Attached)
2 Sockets in /var/run/screen/S-trafgen.
"""


class TestParseListOutput(unittest.TestCase):
    def test_no_session(self):
        result = screen.parse_list_output(NO_SESSION)
        self.assertEqual([], result)

    def test_one_session(self):
        result = screen.parse_list_output(ONE_SESSION)
        self.assertEqual(["pts-1.trafgen"], result)

    def test_two_sessions(self):
        result = screen.parse_list_output(TWO_SESSIONS)
        self.assertEqual(["pts-1.trafgen", "loadtester-call-and-wait"], result)
