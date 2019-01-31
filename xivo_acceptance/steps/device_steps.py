# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that
from hamcrest import equal_to
from hamcrest import is_
from hamcrest import is_not
from hamcrest import none
from lettuce import step, world
from xivo_acceptance.action.webi import device as device_action_webi
from xivo_acceptance.helpers import device_helper, provd_helper, line_read_helper
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
    device_action_webi.search_device(mac)
    common.click_on_line_with_alert('Synchronize', mac)
    device_action_webi.search_device('')


@step(u'^When I search device "([^"]*)"$')
def when_i_search_device(step, search):
    device_action_webi.search_device(search)


@step(u'When I search device by number "([^"]*)"')
def when_i_search_device_by_number(step, number):
    device_action_webi.search_device(number, by_number=True)


@step(u'^When I delete the device with mac "([^"]*)" via webi$')
def when_i_delete_device(step, mac):
    device = provd_helper.get_by_mac(mac)
    common.open_url('device', 'delete', qry={'id': '%s' % device['id']})


@step(u'When I provision device having ip "([^"]*)" with line having username "([^"]*)"')
def when_i_provision_device_having_ip_group1_with_line_having_username_group2(step, device_ip, sip_username):
    line = line_read_helper.find_by_sip_username(sip_username)
    assert_that(line, is_not(none()), "Line with username {} not found".format(sip_username))
    device_helper.provision_device_using_webi(line['provisioning_extension'], device_ip)


@step(u'When I open the edit page of the device with mac "([^"]*)"')
def when_i_open_the_edit_page_of_the_device_with_mac_group1(step, mac):
    device = provd_helper.get_by_mac(mac)
    common.open_url('device', 'edit', qry={'id': device['id']})


@step(u'When I select a plugin "([^"]*)"')
def when_i_select_a_plugin_group1(step, plugin_name):
    device_action_webi.select_plugin(plugin_name)


@step(u'When I check the switchboard checkbox')
def when_i_check_the_switchboard_checkbox(step):
    device_action_webi.check_switchboard()


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
    def assert_device_infos(expected_device):
        actual_device = device_action_webi.get_device_list_entry(expected_device['mac'])
        if 'ip' in expected_device:
            assert_that(actual_device['ip'], equal_to(expected_device['ip']))
        if 'configured' in expected_device:
            expected_configured = expected_device['configured'] == 'True'
            assert_that(actual_device['configured'], equal_to(expected_configured))

    for expected_device in step.hashes:
        common.wait_until_assert(assert_device_infos, expected_device, tries=3)


@step(u'Then the web interfaces shows a device with:')
def then_the_web_interfaces_shows_a_device_with(step):
    device_infos = step.hashes[0]
    if 'switchboard_enabled' in device_infos:
        expected = eval(device_infos['switchboard_enabled'])
        assert_that(device_action_webi.is_switchboard_enabled(), is_(expected))
    if 'switchboard_checked' in device_infos:
        expected = eval(device_infos['switchboard_checked'])
        assert_that(device_action_webi.is_switchboard_checked(), is_(expected))
