# Copyright 2016-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, empty, not_
from behave import then

from wazo_test_helpers import until
from xivo.consul_helpers import ServiceFinder

from ..prerequisite import _configure_consul


@then('consul returns a running "{service_name}" service')
def then_consul_returns_a_running_service(context, service_name):
    # FIXME(afournier): the following should be done differently
    if service_name == 'wazo-setupd':
        _configure_consul(context)

    consul_config = {
        'token': context.wazo_config['consul_token'],
        'scheme': 'http',
        'host': context.wazo_config['wazo_host'],
        'port': 8500,
        'verify': False,
    }
    finder = ServiceFinder(consul_config)

    def service_is_healthy(service_name):
        healthy_services = finder.list_healthy_services(service_name)
        assert_that(healthy_services, not_(empty()))

    until.assert_(
        service_is_healthy, service_name,
        timeout=5,
        message='Service {} not found in Consul'.format(service_name),
    )
