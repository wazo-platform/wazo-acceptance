# -*- coding: utf-8 -*-
# Copyright 2013-2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from lettuce import step, world

from xivo_acceptance.action.webi import provd_general as provdg_action_webi
from xivo_acceptance.lettuce import common

PROXY_FIELDS = ['http_proxy', 'ftp_proxy', 'https_proxy']


@step(u'Given I have no proxies configured')
def given_i_have_no_proxies_configured(step):
    payload = {'param': {'value': None}}
    world.rest_provd.rest_put("/provd/configure/http_proxy", payload)
    world.rest_provd.rest_put("/provd/configure/ftp_proxy", payload)
    world.rest_provd.rest_put("/provd/configure/https_proxy", payload)


@step(u'When I configure the following proxies:')
def when_i_configure_the_following_proxies(step):
    common.open_url('provd_general')
    for config in step.hashes:
        provdg_action_webi.configure_proxies(config)


@step(u'When I reload the provisioning general settings page')
def when_i_reload_the_provisioning_general_settings_page(step):
    common.open_url('provd_general')


@step(u'When I remove all proxy configurations')
def when_i_remove_all_proxy_configurations(step):
    for field in PROXY_FIELDS:
        element = world.browser.find_element_by_name(field)
        element.clear()
        element.send_keys(" ")
        time.sleep(3)


@step(u'Then there are no proxies configured')
def then_there_are_no_proxies_configured(step):
    for field in PROXY_FIELDS:
        element = world.browser.find_element_by_name(field)
        value = element.get_attribute('value')
        assert value == ""
