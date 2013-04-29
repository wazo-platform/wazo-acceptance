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
import sched
import time
from mock import patch
from .. import sysutils


class TestSysUtils(unittest.TestCase):

    def setUp(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def update_mock_return_value(self, mock, return_value):
        mock.return_value = return_value

    @patch('xivo_lettuce.sysutils.is_process_running')
    def test_wait_service_successfully_started(self, mock_is_process_running):
        pidfile = '/tmp/toto'
        mock_is_process_running.return_value = False

        self.scheduler.enter(3, 1, self.update_mock_return_value, (mock_is_process_running, True))
        self.scheduler.run()
        self.assertTrue(sysutils.wait_service_successfully_started(pidfile, maxtries=5, wait_secs=1))

        self.scheduler.enter(3, 1, self.update_mock_return_value, (mock_is_process_running, False))
        self.scheduler.run()
        self.assertFalse(sysutils.wait_service_successfully_started(pidfile, maxtries=5, wait_secs=1))

    @patch('xivo_lettuce.sysutils.is_process_running')
    def test_wait_service_successfully_stopped(self, mock_is_process_running):
        pidfile = '/tmp/toto'
        mock_is_process_running.return_value = True

        self.scheduler.enter(3, 1, self.update_mock_return_value, (mock_is_process_running, False))
        self.scheduler.run()
        self.assertFalse(sysutils.wait_service_successfully_stopped(pidfile, maxtries=5, wait_secs=1))

        self.scheduler.enter(3, 1, self.update_mock_return_value, (mock_is_process_running, True))
        self.scheduler.run()
        self.assertTrue(sysutils.wait_service_successfully_stopped(pidfile, maxtries=5, wait_secs=1))
