import unittest
import os

from pwd import getpwnam


class TestDhcpdUpdate(unittest.TestCase):

    DHCPD_UPDATE_DIR = '/etc/dhcp/dhcpd_update'

    def test_have_dhcpd_update_files(self):
        self.assertTrue(os.access(self.DHCPD_UPDATE_DIR, os.R_OK))
        self.assertTrue(len(os.listdir(self.DHCPD_UPDATE_DIR)) > 0)
