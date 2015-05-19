# -*- coding: utf-8 -*-

# Copyright (C) 2013-2015 Avencall
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

from lettuce import step, world
from hamcrest import assert_that, equal_to, is_, none, \
    has_entry, has_entries, has_item, has_length, \
    contains_string, instance_of
from xivo_acceptance.action.webi import provd_plugins
from xivo_acceptance.action.confd import device_action_confd
from xivo_acceptance.action.webi import device as device_action_webi
from xivo_acceptance.helpers import device_helper, provd_helper, line_sip_helper
from xivo_dao.resources.line import dao as line_dao
from xivo_acceptance.lettuce import form, common, logs, sysutils


@step(u'Given there are no devices with mac "([^"]*)"')
def given_there_are_no_devices_with_mac_group1(step, mac):
    provd_helper.delete_device_with_mac(mac)


@step(u'Given there are no devices with id "([^"]*)"')
def given_there_are_no_devices_with_id_group1(step, device_id):
    provd_helper.delete_device(device_id)


@step(u'Given I have the following devices:')
def given_i_have_the_following_devices(step):
    for deviceinfo in step.hashes:
        if 'latest plugin of' in deviceinfo:
            deviceinfo = dict(deviceinfo)
            deviceinfo['plugin'] = provd_plugins.get_latest_plugin_name(deviceinfo['latest plugin of'])
            del deviceinfo['latest plugin of']
        device_id = device_helper.add_or_replace_device(deviceinfo)
        device_action_confd.reset_to_autoprov(device_id)


@step(u'Given there exists the following device templates:')
def given_there_exists_the_following_device_template(step):
    for template in step.hashes:
        provd_helper.add_or_replace_device_template(template)


@step(u'Given I set the HTTP_PROXY environment variables to "([^"]*)"')
def given_i_set_the_http_proxy_environment_variables_to_group1(step, http_proxy):
    sysutils.restart_service('xivo-confd', env={'HTTP_PROXY': http_proxy})


@step(u'Given device with ip "([^"]*)" is provisionned with SIP line "([^"]*)"')
def given_device_with_mac_group1_is_provisionned_with_sip_line_group2(step, device_ip, sip_username):
    line = line_sip_helper.get_by_username(sip_username)
    device_helper.provision_device_using_webi(line['provisioning_extension'], device_ip)


@step(u'Given the provisioning server has received the following HTTP requests:')
def given_the_provisioning_server_has_received_the_following_http_requests(step):
    _provisioning_server_http_requests(step)


@step(u'When the provisioning server receives the following HTTP requests:')
def when_the_provisioning_server_receives_the_following_http_requests(step):
    _provisioning_server_http_requests(step)


def _provisioning_server_http_requests(step):
    for request_data in step.hashes:
        provd_helper.request_http(request_data['path'], request_data['user-agent'])


@step(u'When I create an empty device$')
def when_i_create_an_empty_device(step):
    world.response = device_action_confd.create_device({})


@step(u'When I create the following devices:')
def when_i_create_the_following_devices(step):
    for device in step.hashes:
        _update_device_from_step_hash(device)
        world.response = device_action_confd.create_device(device)


@step(u'When I create a device using the device template id "([^"]*)"')
def when_i_create_a_device_using_the_device_template_id_group1(step, device_template_id):
    device = {
        'template_id': device_template_id
    }
    world.response = device_action_confd.create_device(device)


@step(u'When I delete the device with mac "([^"]*)" from confd$')
def when_i_delete_the_device(step, mac):
    device = provd_helper.get_by_mac(mac)
    world.deleted_device = device
    world.response = device_action_confd.delete_device(device['id'])


@step(u'When I associate my line_id "([^"]*)" to the device "([^"]*)"')
def when_i_associate_my_line_id_to_the_device(step, line_id, device_id):
    world.response = device_action_confd.associate_line_to_device(device_id, line_id)


@step(u'^When I synchronize the device with mac "([^"]*)" from confd$')
def when_i_synchronize_the_device_group1_from_confd(step, mac):
    device = provd_helper.get_by_mac(mac)
    world.response = device_action_confd.synchronize(device['id'])


@step(u'When I go get the device with mac "([^"]*)" using its id')
def when_i_go_get_the_device_with_mac_group1_using_its_id(step, mac):
    device = provd_helper.get_by_mac(mac)
    world.response = device_action_confd.get_device(device['id'])


@step(u'When I request the list of devices')
def when_i_access_the_list_of_devices(step):
    world.response = device_action_confd.device_list()


@step(u'When I reset the device with mac "([^"]*)" to autoprov from confd')
def when_i_reset_the_device_to_autoprov_from_confd(step, mac):
    device = provd_helper.get_by_mac(mac)
    world.response = device_action_confd.reset_to_autoprov(device['id'])


@step(u'When I remove line_id "([^"]*)" from device "([^"]*)"')
def when_i_remove_line_id_group1_from_device_group2(step, line_id, device_id):
    world.response = device_action_confd.remove_line_from_device(device_id, line_id)


@step(u'When I edit the device with mac "([^"]*)" using no parameters')
def when_i_edit_the_device_with_mac_group1_using_no_parameters(step, mac):
    device = provd_helper.get_by_mac(mac)
    world.response = device_action_confd.edit_device(device['id'], {})


@step(u'When I edit the device with mac "([^"]*)" using the following parameters:')
def when_i_edit_the_device_with_mac_group1_using_the_following_parameters(step, mac):
    device = provd_helper.get_by_mac(mac)
    parameters = step.hashes[0]
    world.response = device_action_confd.edit_device(device['id'], parameters)


@step(u'When I request devices in the webi')
def when_i_request_devices_in_the_webi(step):
    common.open_url('device')


@step(u'When I synchronize the device with mac "([^"]*)" from webi')
def when_i_synchronize_the_device_group1_from_webi(step, mac):
    device_action_webi.search_device(mac)
    common.click_on_line_with_alert('Synchronize', mac)
    device_action_webi.search_device('')


@step(u'When I reset to autoprov the device with mac "([^"]*)" from webi')
def when_i_reset_to_autoprov_the_device_from_webi(step, mac):
    device_action_webi.search_device(mac)
    common.click_on_line_with_alert('Reset to autoprov mode', mac)
    device_action_webi.search_device('')


@step(u'^When I search device "([^"]*)"$')
def when_i_search_device(step, search):
    device_action_webi.search_device(search)


@step(u'When I search device by number "([^"]*)"')
def when_i_search_device_by_number(step, number):
    device_action_webi.search_device(number, by_number=True)


@step(u'When I create the device with infos:')
def when_i_create_the_device_with_infos(step):
    common.open_url('device', 'add')
    device_infos = step.hashes[0]
    if 'mac' in device_infos:
        provd_helper.delete_device_with_mac(device_infos['mac'])
        device_action_webi.type_input('mac', device_infos['mac'])
    if 'ip' in device_infos:
        provd_helper.delete_device_with_ip(device_infos['ip'])
        device_action_webi.type_input('ip', device_infos['ip'])
    if 'plugin' in device_infos:
        device_action_webi.type_input('plugin', device_infos['plugin'])
    if 'template_id' in device_infos:
        device_action_webi.type_select('template_id', device_infos['template_id'])
    form.submit.submit_form()


@step(u'When I edit the device with mac "([^"]*)" via webi with infos:')
def when_i_edit_the_device_with_mac_via_webi_with_infos(step, mac):
    device = provd_helper.get_by_mac(mac)
    common.open_url('device', 'edit', qry={'id': device['id']})
    device_infos = step.hashes[0]
    if 'plugin' in device_infos:
        device_action_webi.type_input('plugin', device_infos['plugin'])
    if 'template_id' in device_infos:
        device_action_webi.type_select('template_id', device_infos['template_id'])
    if 'description' in device_infos:
        device_action_webi.type_input('description', device_infos['description'])
    form.submit.submit_form()


@step(u'^When I delete the device with mac "([^"]*)" via webi$')
def when_i_delete_device(step, mac):
    device = provd_helper.get_by_mac(mac)
    common.open_url('device', 'delete', qry={'id': '%s' % device['id']})


@step(u'When I provision my device with my line_id "([^"]*)" and ip "([^"]*)"')
def when_i_provision_my_device_with_my_line_id_group1(step, line_id, device_ip):
    line = line_dao.get(line_id)
    device_helper.provision_device_using_webi(line.provisioning_extension, device_ip)


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


@step(u'Then I see in the log file device with mac "([^"]*)" synchronized')
def then_i_see_in_the_log_file_device_synchronized(step, mac):
    device = provd_helper.get_by_mac(mac)
    expected_log_lines = ['Synchronizing device %s' % device['id']]
    actual_log_lines = logs.find_line_in_xivo_provd_log()
    _assert_all_lines_in_log(actual_log_lines, expected_log_lines)


@step(u'Then I see in the log file device with mac "([^"]*)" autoprovisioned')
def then_i_see_in_the_log_file_device_group1_autoprovisioned(step, mac):
    device = provd_helper.get_by_mac(mac)
    expected_log_lines = ['Creating new config',
                          '/provd/cfg_mgr/autocreate',
                          'Updating device',
                          '/provd/dev_mgr/devices/%s' % device['id']]
    actual_log_lines = logs.find_line_in_xivo_provd_log()
    _assert_all_lines_in_log(actual_log_lines, expected_log_lines)


@step(u'Then the device with mac "([^"]*)" is no longer exists in provd')
def then_the_device_is_no_longer_exists_in_provd(step, mac):
    device = provd_helper.find_by_mac(mac)
    assert_that(device, none(), "Device still exists in provd")


@step(u'Then I see in the log file that the device was deleted')
def then_i_see_in_the_log_file_device_deleted(step):
    device_id = world.deleted_device['id']
    expected_log_lines = ['Deleting device %s' % device_id,
                          '/provd/dev_mgr/devices/%s' % device_id,
                          'Deleting config %s' % device_id,
                          '/provd/cfg_mgr/configs/%s' % device_id]
    actual_log_lines = logs.find_line_in_xivo_provd_log()
    _assert_all_lines_in_log(actual_log_lines, expected_log_lines)


def _assert_all_lines_in_log(actual_log, expected_lines):
    for expected_line in expected_lines:
        assert_that(actual_log, has_item(contains_string(expected_line)))


@step(u'Then the web interfaces shows a device with:')
def then_the_web_interfaces_shows_a_device_with(step):
    device_infos = step.hashes[0]
    if 'switchboard_enabled' in device_infos:
        expected = eval(device_infos['switchboard_enabled'])
        assert_that(device_action_webi.is_switchboard_enabled(), is_(expected))
    if 'switchboard_checked' in device_infos:
        expected = eval(device_infos['switchboard_checked'])
        assert_that(device_action_webi.is_switchboard_checked(), is_(expected))


@step(u'Then I get a response with a device id')
def then_i_get_a_response_with_a_device_id(step):
    assert_that(world.response.data,
                has_entry('id', has_length(32)))


@step(u'Then the device has the following parameters:')
def then_the_device_has_the_following_parameters(step):
    device_response = world.response.data
    expected_device = step.hashes[0]
    _update_device_from_step_hash(expected_device)

    assert_that(device_response, has_entries(expected_device))


@step(u'Then I get a list containing the following devices:')
def then_i_get_a_list_containing_the_following_devices(step):
    assert_that(world.response.data, has_entries(
        'total', instance_of(int),
        'items', instance_of(list)))

    device_list = world.response.data['items']

    for device in step.hashes:
        _update_device_from_step_hash(device)
        assert_that(device_list, has_item(has_entries(device)))


@step(u'Then the list contains the same number of devices as on the provisioning server')
def then_the_list_contains_the_same_number_of_devices_as_on_the_provisioning_server(step):
    total_provd = provd_helper.total_devices()

    device_list = world.response.data['items']

    assert_that(device_list, has_length(total_provd))


def _update_device_from_step_hash(device):
    if 'options' in device:
        device['options'] = eval(device['options'])
    if 'template_id' in device and device['template_id'] == u'None':
        device['template_id'] = None
