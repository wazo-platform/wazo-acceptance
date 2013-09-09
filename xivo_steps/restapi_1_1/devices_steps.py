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

from xivo_lettuce.restapi.v1_1 import device_helper, provd_helper
from xivo_lettuce.manager_restapi import device_ws

from hamcrest import assert_that, has_entries, has_entry, has_length
from lettuce import step, world


@step(u'Given I have no devices')
def given_there_are_no_devices(step):
    device_helper.delete_all()


@step(u'Given there are no devices with mac "([^"]*)"')
def given_there_are_no_devices_with_mac_group1(step, mac):
    provd_helper.delete_device_with_mac(mac)


@step(u'Given there are no devices with id "([^"]*)"')
def given_there_are_no_devices_with_id_group1(step, device_id):
    provd_helper.delete_device(device_id)


@step(u'Given I only have the following devices:')
def given_there_are_the_following_devices(step):
    device_helper.delete_all()
    for deviceinfo in step.hashes:
        device_helper.create_device(deviceinfo)


@step(u'Given I have the following devices:')
def given_i_have_the_following_devices(step):
    for deviceinfo in step.hashes:
        device_helper.create_device(deviceinfo)


@step(u'Given there exists the following device templates:')
def given_there_exists_the_following_device_template(step):
    for template in step.hashes:
        provd_helper.add_or_replace_device_template(template)


@step(u'When I create an empty device')
def when_i_create_an_empty_device(step):
    world.response = device_ws.create_device({})


@step(u'When I create the following devices:')
def when_i_create_the_following_devices(step):
    for device_info in step.hashes:
        world.response = device_ws.create_device(device_info)


@step(u'When I create a device using the device template id "([^"]*)"')
def when_i_create_a_device_using_the_device_template_id_group1(step, device_template_id):
    device = {
        'template_id': device_template_id
    }
    world.response = device_ws.create_device(device)


@step(u'^When I synchronize the device "([^"]*)" from restapi$')
def when_i_synchronize_the_device_group1_from_restapi(step, device_id):
    world.response = device_ws.synchronize(device_id)


@step(u'When I provision my device "([^"]*)" with my line "([^"]*)"')
def when_i_provision_my_device_group1_with_my_line_group2(step, device_mac, line_id):
    assert False, 'This step must be implemented'


@step(u'Then I get a response with a device id')
def then_i_get_a_response_with_a_device_id(step):
    assert_that(world.response.data,
                has_entry('id', has_length(32)))


@step(u'Then the created device has the following parameters:')
def then_the_created_device_has_the_following_parameters(step):
    device_response = world.response.data
    expected_device = step.hashes[0]

    assert_that(device_response, has_entries(expected_device))
