# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, empty, not_
from behave import then

from xivo_test_helpers import until
from xivo.consul_helpers import ServiceFinder


@then('consul returns a running "{service_name}" service')
def consul_returns_a_running_service(context, service_name):
    consul_config = {'token': context.wazo_config['consul_token'],
                     'scheme': 'https',
                     'host': context.wazo_config['wazo_host'],
                     'port': 8500,
                     'verify': False}
    finder = ServiceFinder(consul_config)

    def test():
        healthy_services = finder.list_healthy_services(service_name)
        assert_that(healthy_services, not_(empty()))

    until.assert_(test, tries=5)
