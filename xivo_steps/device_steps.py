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

from lettuce import step
from hamcrest import *
from urllib2 import HTTPError

from xivo_acceptance.action.webi import device as device_action_webi
from xivo_acceptance.helpers import device_helper, provd_helper
from xivo_dao.data_handler.line import dao as line_dao
from xivo_lettuce import form, common, logs


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


@step(u'When I edit the device "([^"]*)" with infos:')
def when_i_edit_the_device_with_infos(step, device_id):
    common.open_url('device', 'edit', qry={'id': device_id})
    device_infos = step.hashes[0]
    if 'plugin' in device_infos:
        device_action_webi.type_input('plugin', device_infos['plugin'])
    if 'template_id' in device_infos:
        device_action_webi.type_select('template_id', device_infos['template_id'])
    if 'description' in device_infos:
        device_action_webi.type_input('description', device_infos['description'])
    form.submit.submit_form()


@step(u'^When I delete the device "([^"]*)"$')
def when_i_delete_device(step, device_id):
    common.open_url('device', 'delete', qry={'id': '%s' % device_id})


@step(u'When I provision my device with my line_id "([^"]*)" and ip "([^"]*)"')
def when_i_provision_my_device_with_my_line_id_group1(step, line_id, device_ip):
    line = line_dao.get(line_id)
    device_helper.provision_device_using_webi(line.provisioning_extension, device_ip)


@step(u'When I open the edit page of the device "([^"]*)"')
def when_i_open_the_edit_page_of_the_device_group1(step, device_id):
    common.open_url('device', 'edit', qry={'id': device_id})


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


@step(u'Then the device "([^"]*)" has been provisioned with a configuration:')
def then_the_device_has_been_provisioned_with_a_configuration(step, device_id):
    provd_helper.device_config_has_properties(device_id, step.hashes)


@step(u'Then I see devices with infos:')
def then_i_see_devices_with_infos(step):
    for expected_device in step.hashes:
        actual_device = device_action_webi.get_device_list_entry(expected_device['mac'])
        if 'ip' in expected_device:
            assert_that(actual_device['ip'], equal_to(expected_device['ip']))
        if 'configured' in expected_device:
            expected_configured = expected_device['configured'] == 'True'
            assert_that(actual_device['configured'], equal_to(expected_configured))


@step(u'Then I see in the log file device "([^"]*)" synchronized')
def then_i_see_in_the_log_file_device_synchronized(step, device_id):
    expected_log_lines = ['Synchronizing device %s' % device_id]
    actual_log_lines = logs.find_line_in_xivo_provd_log()
    _assert_all_lines_in_log(actual_log_lines, expected_log_lines)


@step(u'Then I see in the log file device "([^"]*)" autoprovisioned')
def then_i_see_in_the_log_file_device_group1_autoprovisioned(step, device_id):
    expected_log_lines = ['Creating new config',
                          '/provd/cfg_mgr/autocreate',
                          'Updating device',
                          '/provd/dev_mgr/devices/%s' % device_id]
    actual_log_lines = logs.find_line_in_xivo_provd_log()
    _assert_all_lines_in_log(actual_log_lines, expected_log_lines)


@step(u'Then the device "([^"]*)" is no longer exists in provd')
def then_the_device_is_no_longer_exists_in_provd(step, device_id):
    try:
        provd_helper.get_device(device_id)
    except HTTPError:
        assert True
    else:
        assert False, 'The device %s is longer exists in provd' % device_id


@step(u'Then I see in the log file device "([^"]*)" deleted')
def then_i_see_in_the_log_file_device_deleted(step, device_id):
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
