# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step, world


@step(u'Given I have no proxies configured')
def given_i_have_no_proxies_configured(step):
    payload = {'param': {'value': None}}
    world.rest_provd.rest_put("/provd/configure/http_proxy", payload)
    world.rest_provd.rest_put("/provd/configure/ftp_proxy", payload)
    world.rest_provd.rest_put("/provd/configure/https_proxy", payload)


@step(u'When I configure the following proxies:')
def when_i_configure_the_following_proxies(step):
    pass


@step(u'When I reload the provisioning general settings page')
def when_i_reload_the_provisioning_general_settings_page(step):
    pass


@step(u'When I remove all proxy configurations')
def when_i_remove_all_proxy_configurations(step):
    pass


@step(u'Then there are no proxies configured')
def then_there_are_no_proxies_configured(step):
    pass
