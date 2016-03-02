# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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
        element.send_keys("\b")
        time.sleep(3)


@step(u'Then there are no proxies configured')
def then_there_are_no_proxies_configured(step):
    for field in PROXY_FIELDS:
        element = world.browser.find_element_by_name(field)
        value = element.get_attribute('value')
        assert value == ""
