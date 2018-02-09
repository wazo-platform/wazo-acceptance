# -*- coding: utf-8 -*-
# Copyright (C) 2016 Proformatique, Inc.
# SPDX-License-Identifier: GPL-3.0+

from hamcrest import assert_that, empty, not_
from lettuce import step, world

from xivo_test_helpers import until
from xivo.consul_helpers import ServiceFinder


@step(u'Then consul returns a running "([^"]*)" service')
def then_consul_returns_a_running_service(step, service_name):
    consul_config = {'token': world.config['consul_token'],
                     'scheme': 'https',
                     'host': world.config['xivo_host'],
                     'port': 8500,
                     'verify': False}
    finder = ServiceFinder(consul_config)

    def test():
        healthy_services = finder.list_healthy_services(service_name)
        assert_that(healthy_services, not_(empty()))

    until.assert_(test, tries=5)
