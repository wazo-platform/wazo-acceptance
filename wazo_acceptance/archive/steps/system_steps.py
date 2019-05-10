# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that
from hamcrest import is_
from lettuce import step

from xivo_acceptance.helpers import directory_helper
from xivo_acceptance.lettuce import sysutils


@step(u'I restart "([^"]*)"$')
def i_restart_service(step, service_name):
    sysutils.restart_service(service_name)


@step(u'I restart wazo-dird$')
def i_restart_wazo_dird(step):
    directory_helper.restart_dird()


@step(u'Then the service "([^"]*)" is running')
def then_the_service_group1_is_running(step, service):
    pidfile = sysutils.get_pidfile_for_service_name(service)
    assert sysutils.is_process_running(pidfile)


@step(u'Then the file "([^"]*)" does not exist')
def then_the_file_1_does_not_exist(step, file_name):
    assert_that(sysutils.path_exists(file_name), is_(False))
