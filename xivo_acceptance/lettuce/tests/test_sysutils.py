# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

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

    @patch('xivo_acceptance.lettuce.sysutils.is_process_running')
    def test_wait_service_successfully_started(self, mock_is_process_running):
        pidfile = '/tmp/toto'
        mock_is_process_running.return_value = False

        self.scheduler.enter(3, 1, self.update_mock_return_value, (mock_is_process_running, True))
        self.scheduler.run()
        self.assertTrue(sysutils.wait_service_successfully_started(pidfile, maxtries=5, wait_secs=1))

        self.scheduler.enter(3, 1, self.update_mock_return_value, (mock_is_process_running, False))
        self.scheduler.run()
        self.assertFalse(sysutils.wait_service_successfully_started(pidfile, maxtries=5, wait_secs=1))

    @patch('xivo_acceptance.lettuce.sysutils.is_process_running')
    def test_wait_service_successfully_stopped(self, mock_is_process_running):
        pidfile = '/tmp/toto'
        mock_is_process_running.return_value = True

        self.scheduler.enter(3, 1, self.update_mock_return_value, (mock_is_process_running, False))
        self.scheduler.run()
        self.assertFalse(sysutils.wait_service_successfully_stopped(pidfile, maxtries=5, wait_secs=1))

        self.scheduler.enter(3, 1, self.update_mock_return_value, (mock_is_process_running, True))
        self.scheduler.run()
        self.assertTrue(sysutils.wait_service_successfully_stopped(pidfile, maxtries=5, wait_secs=1))
