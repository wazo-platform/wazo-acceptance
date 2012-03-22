import unittest
import os

from pwd import getpwnam


class TestVoiceMailEmpty(unittest.TestCase):

    ASTERISK_VM_PATH = '/var/spool/asterisk/voicemail'

    def test_voicemail_dir_empty(self):
        self.assertTrue(os.path.exists(self.ASTERISK_VM_PATH))
        self.assertEqual(len(os.listdir(self.ASTERISK_VM_PATH)), 0)


class TestSoundsInstalled(unittest.TestCase):

    ASTERISK_SOUND_PATH = '/usr/share/asterisk/sounds/en'

    def test_sounds_file_are_installed(self):
        self.assertTrue(os.path.exists(self.ASTERISK_SOUND_PATH))
        self.assertFalse(len(os.listdir(self.ASTERISK_SOUND_PATH)) == 0)


class TestAsteriskOwnsDahdi(unittest.TestCase):

    DAHDI_PATH = '/dev/dahdi'

    def test_asterisk_owns_dahdi_files(self):
        self.assertTrue(os.path.exists(self.DAHDI_PATH))
        for file in os.listdir(self.DAHDI_PATH):
            self.assertTrue(self._owned_by_asterisk(os.path.sep.join([self.DAHDI_PATH, file])))

    def _owned_by_asterisk(self, file):
        asterisk_ids = getpwnam('asterisk')[2:4]
        file_ids = os.stat(file)[4:6]
        return asterisk_ids == file_ids


class TestDhcpdUpdate(unittest.TestCase):

    DHCPD_UPDATE_DIR = '/etc/dhcp/dhcpd_update'

    def test_have_dhcpd_update_files(self):
        self.assertTrue(os.access(self.DHCPD_UPDATE_DIR, os.R_OK))
        self.assertTrue(len(os.listdir(self.DHCPD_UPDATE_DIR)) > 0)
