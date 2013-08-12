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

from lettuce import step
from hamcrest import assert_that, equal_to
from xivo_lettuce.manager import device_manager
from xivo_lettuce.manager import provd_client
from xivo_lettuce import postgres


@step(u'^Given there is a device with infos:$')
def given_there_is_a_device_with_infos(step):
    for info in step.hashes:
        device_manager.add_or_replace_device(info)


@step(u'^When I search device "([^"]*)"$')
def when_i_search_device(step, search):
    device_manager.search_device(search)


@step(u'Given there is a device in autoprov with infos:')
def given_there_is_a_device_in_autoprov_with_infos(step):
    device_properties = step.hashes[0]
    mac_address = device_properties['mac']
    plugin = device_properties['plugin']

    provd_client.delete_device_by_mac(mac_address)
    postgres.exec_sql_request('delete from devicefeatures where mac = \'%s\'' % mac_address)

    provd_client.create_device(
        mac_address=mac_address,
        plugin=plugin
    )


@step(u'Then I see devices with infos:')
def then_i_see_devices_with_infos(step):
    for expected_device in step.hashes:
        actual_device = device_manager.get_device_list_entry(expected_device['mac'])
        if 'ip' in expected_device:
            assert_that(actual_device['ip'], equal_to(expected_device['ip']))
        if 'configured' in expected_device:
            expected_configured = expected_device['configured'] == 'True'
            assert_that(actual_device['configured'], equal_to(expected_configured))
