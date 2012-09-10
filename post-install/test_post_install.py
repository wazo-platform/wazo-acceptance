# -*- coding: UTF-8 -*-

import unittest
import os
import subprocess
import pwd
import grp
import sys

from pwd import getpwnam


class TestVoiceMailEmpty(unittest.TestCase):

    ASTERISK_VM_PATH = '/var/spool/asterisk/voicemail'

    def test_voicemail_dir_empty(self):
        self.assertTrue(os.path.isdir(self.ASTERISK_VM_PATH))
        self.assertEqual(len(os.listdir(self.ASTERISK_VM_PATH)), 0)


class TestSoundsInstalled(unittest.TestCase):

    ASTERISK_SOUND_PATH = '/usr/share/asterisk/sounds/en'

    def test_sounds_file_are_installed(self):
        self.assertTrue(os.path.isdir(self.ASTERISK_SOUND_PATH))
        self.assertTrue(len(os.listdir(self.ASTERISK_SOUND_PATH)) > 0)


class TestAsteriskOwnsDahdi(unittest.TestCase):

    DAHDI_PATH = '/dev/dahdi'

    def test_asterisk_owns_dahdi_files(self):
        self.assertTrue(os.path.isdir(self.DAHDI_PATH))
        for file in os.listdir(self.DAHDI_PATH):
            self.assertTrue(self._owned_by_asterisk(os.path.join(self.DAHDI_PATH, file)))

    def _owned_by_asterisk(self, file):
        asterisk_ids = getpwnam('asterisk')[2:4]
        file_ids = os.stat(file)[4:6]
        return asterisk_ids == file_ids


class TestMohFilesPermission(unittest.TestCase):

    MOH_PATH = '/usr/share/asterisk/moh/default'
    MOH_PKG = 'asterisk-moh-opsound-wav'
    FILE_UID = 'asterisk'
    FILE_GID = 'www-data'

    def test_files_are_installed(self):
        command = ['apt-get', 'install', self.MOH_PKG]
        _exec_local_cmd(command)

    def test_files_owned_by_asterisk(self):
        files = os.listdir(self.MOH_PATH)

        for file in files:
            file_path = os.path.join(self.MOH_PATH, file)
            uid = self._find_uid(file_path)
            gid = self._find_gid(file_path)
            self.assertEqual(self.FILE_UID, uid, 'File %s : UID %s not owned by %s ' % (file, uid, self.FILE_UID))
            self.assertEqual(self.FILE_GID, gid, 'File %s : GID %s not owned by %s ' % (file, gid, self.FILE_GID))


    def _find_uid(self, file):
        return pwd.getpwuid(os.stat(file).st_uid).pw_name

    def _find_gid(self, file):
        return grp.getgrgid(os.stat(file).st_gid).gr_name


class TestBackupLogRotate(unittest.TestCase):

    BACKUP_DIR = '/var/backups/pf-xivo/'

    def setUp(self):
        files = os.listdir(self.BACKUP_DIR)
        for file in files:
            file_path = os.path.join(self.BACKUP_DIR, file)
            os.remove(file_path)
        data_file = os.path.join(self.BACKUP_DIR, 'data.tgz')
        db_file = os.path.join(self.BACKUP_DIR, 'db.tgz')
        open(data_file, 'w+')
        open(db_file, 'w+')
        del sys.path

    def test_backup_rotate_files(self):
        self._exec_logrotate_backup()
        expected_files = ['data.tgz', 'data.tgz.1', 'db.tgz', 'db.tgz.1']

        for expected_file in expected_files:
            file_path = os.path.join(self.BACKUP_DIR, expected_file)
            self.assertTrue(self._is_file_exist(file_path))

        self._exec_logrotate_backup()
        expected_files.extend(['data.tgz.2', 'db.tgz.2'])

        for expected_file in expected_files:
            file_path = os.path.join(self.BACKUP_DIR, expected_file)
            self.assertTrue(self._is_file_exist(file_path))

    def _exec_logrotate_backup(self):
        command = ['/usr/sbin/logrotate', '-f', '/etc/logrotate.d/pf-xivo-backup']
        _exec_local_cmd(command)

    def _is_file_exist(self, path):
        print path
        try:
           with open(path) as f:
               return True
        except IOError as e:
           return False


def _exec_local_cmd(cmd):
        p = subprocess.Popen(cmd,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             close_fds=True)

        (stdoutdata, stderrdata) = p.communicate()

        if p.returncode != 0:
            print stdoutdata
            print stderrdata
            assert(False)
