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

from hamcrest import *
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
        if 'mac' in deviceinfo:
            provd_helper.delete_device_with_mac(deviceinfo['mac'])
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


@step(u'When I associate my line_id "([^"]*)" to the device "([^"]*)"')
def when_i_associate_my_line_id_to_the_device(step, line_id, device_id):
    world.response = device_ws.associate_line_to_device(device_id, line_id)


@step(u'^When I synchronize the device "([^"]*)" from restapi$')
def when_i_synchronize_the_device_group1_from_restapi(step, device_id):
    world.response = device_ws.synchronize(device_id)


@step(u'When I provision my device "([^"]*)" with my line "([^"]*)"')
def when_i_provision_my_device_group1_with_my_line_group2(step, device_mac, line_id):
    assert False, 'This step must be implemented'


@step(u'When I go get the device with id "([^"]*)"')
def when_i_go_get_the_device_with_id_group1(step, device_id):
    world.response = device_ws.get_device(device_id)


@step(u'When I go get the device with mac "([^"]*)" using its id')
def when_i_go_get_the_device_with_mac_group1_using_its_id(step, mac):
    device = provd_helper.find_by_mac(mac)
    world.response = device_ws.get_device(device['id'])


@step(u'When I request the list of devices')
def when_i_access_the_list_of_devices(step):
    world.response = device_ws.device_list()


@step(u'When I request a list of devices with the following query parameters:')
def when_i_request_a_list_of_devices_with_the_following_query_parameters(step):
    parameters = step.hashes[0]
    world.response = device_ws.device_list(parameters)


@step(u'When I reset the device "([^"]*)" to autoprov from restapi')
def when_i_reset_the_device_to_autoprov_from_restapi(step, device_id):
    world.response = device_ws.reset_to_autoprov(device_id)


@step(u'Then I get a response with a device id')
def then_i_get_a_response_with_a_device_id(step):
    assert_that(world.response.data,
                has_entry('id', has_length(32)))


@step(u'Then the device has the following parameters:')
def then_the_device_has_the_following_parameters(step):
    device_response = world.response.data
    expected_device = step.hashes[0]

    assert_that(device_response, has_entries(expected_device))


@step(u'Then I get a list containing the following devices:')
def then_i_get_a_list_containing_the_following_devices(step):
    assert_that(world.response.data, has_entries(
        'total', instance_of(int),
        'items', instance_of(list)))

    device_list = world.response.data['items']

    for device in step.hashes:
        assert_that(device_list, has_item(has_entries(device)))


@step(u'Then the list contains the same number of devices as on the provisioning server')
def then_the_list_contains_the_same_number_of_devices_as_on_the_provisioning_server(step):
    total_provd = provd_helper.total_devices()

    device_list = world.response.data['items']
    total = world.response.data['total']

    assert_that(total_provd, equal_to(total))
    assert_that(device_list, has_length(total_provd))


@step(u'Then I get a list of devices in the following order:')
def then_i_get_a_list_of_devices_in_the_following_order(step):
    matching_devices = _extract_matching_devices(step.hashes)
    assert_that(matching_devices, _contains_all_devices(step.hashes))


def _contains_all_devices(devices):
    return contains(*_all_items(devices))


def _extract_matching_devices(devices):
    matcher = any_of(*_all_items(devices))
    return [device for device in devices if matcher.matches(device)]


def _all_items(devices):
    return [has_entries(device) for device in devices]


@step(u'Given I only have (\d+) devices')
def given_i_only_have_n_devices(step, nb_devices):
    nb_devices = int(nb_devices)
    provd_helper.remove_devices_over(nb_devices)

    total_devices = provd_helper.total_devices()
    if total_devices < nb_devices:
        device_helper.create_dummy_devices(nb_devices - total_devices)


@step(u'Then I get a list with (\d+) devices')
def then_i_get_a_list_with_5_devices(step, nb_devices):
    nb_devices = int(nb_devices)
    assert_that(world.response.data, all_of(
        has_entry('total', nb_devices),
        has_entry('items', has_length(nb_devices))))


@step(u'Given I have at least (\d+) dummy devices')
def given_i_have_at_least_30_dummy_devices(step, nb_devices):
    nb_devices = int(nb_devices)
    device_helper.create_dummy_devices(nb_devices)
