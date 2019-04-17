# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step, world
from xivo_acceptance.helpers import device_helper, provd_helper
from xivo_acceptance.lettuce import common


@step(u'Given there are no devices with mac "([^"]*)"')
def given_there_are_no_devices_with_mac_group1(step, mac):
    provd_helper.delete_device_with_mac(mac)


@step(u'Given I have the following devices:')
def given_i_have_the_following_devices(step):
    for deviceinfo in step.hashes:
        if 'latest plugin of' in deviceinfo:
            deviceinfo = dict(deviceinfo)
            deviceinfo['plugin'] = provd_helper.get_latest_plugin_name(deviceinfo['latest plugin of'])
            del deviceinfo['latest plugin of']
        device = device_helper.add_or_replace_device(deviceinfo)
        world.confd_client.devices.autoprov(device['id'])


@step(u'Given the provisioning server has received the following HTTP requests:')
def given_the_provisioning_server_has_received_the_following_http_requests(step):
    _provisioning_server_http_requests(step)


@step(u'When the provisioning server receives the following HTTP requests:')
def when_the_provisioning_server_receives_the_following_http_requests(step):
    _provisioning_server_http_requests(step)


def _provisioning_server_http_requests(step):
    for request_data in step.hashes:
        provd_helper.request_http(request_data['path'], request_data['user-agent'])


@step(u'When I synchronize the device with mac "([^"]*)" from webi')
def when_i_synchronize_the_device_group1_from_webi(step, mac):
    pass


@step(u'^When I search device "([^"]*)"$')
def when_i_search_device(step, search):
    pass


@step(u'When I search device by number "([^"]*)"')
def when_i_search_device_by_number(step, number):
    pass


@step(u'^When I delete the device with mac "([^"]*)" via webi$')
def when_i_delete_device(step, mac):
    pass


@step(u'When I provision device having ip "([^"]*)" with line having username "([^"]*)"')
def when_i_provision_device_having_ip_group1_with_line_having_username_group2(step, device_ip, sip_username):
    pass


@step(u'When I open the edit page of the device with mac "([^"]*)"')
def when_i_open_the_edit_page_of_the_device_with_mac_group1(step, mac):
    pass


@step(u'When I select a plugin "([^"]*)"')
def when_i_select_a_plugin_group1(step, plugin_name):
    pass


@step(u'When I check the switchboard checkbox')
def when_i_check_the_switchboard_checkbox(step):
    pass


@step(u'Then there is no device "([^"]*)"')
def then_there_is_no_device(step, search):
    query = {'search': search}
    assert common.element_is_not_in_list('device', search, query)


@step(u'Then the device with mac "([^"]*)" has been provisioned with a configuration:')
def then_the_device_with_mac_has_been_provisioned_with_a_configuration(step, mac):
    device = provd_helper.get_by_mac(mac)
    provd_helper.device_config_has_properties(device['id'], step.hashes[0])


@step(u'Then I see devices with infos:')
def then_i_see_devices_with_infos(step):
    pass


@step(u'Then the web interfaces shows a device with:')
def then_the_web_interfaces_shows_a_device_with(step):
    pass
