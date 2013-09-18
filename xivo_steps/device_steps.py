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
from hamcrest import assert_that, equal_to, is_not, has_key, starts_with
from xivo_lettuce.manager import device_manager
from xivo_lettuce.manager import provd_cfg_dev_manager
from xivo_lettuce import form, common, logs
from xivo_lettuce.restapi.v1_1 import device_helper

from xivo_dao.data_handler.line import dao as line_dao
from urllib2 import HTTPError


@step(u'When I request devices in the webi')
def when_i_request_devices_in_the_webi(step):
    common.open_url('device')


@step(u'When I synchronize the device with mac "([^"]*)" from webi')
def when_i_synchronize_the_device_group1_from_webi(step, mac):
    common.open_url('device', 'search', {'search': '%s' % mac})
    common.click_on_line_with_alert('Synchronize', mac)
    common.open_url('device', 'search', {'search': ''})


@step(u'When I reset to autoprov the device with mac "([^"]*)" from webi')
def when_i_reset_to_autoprov_the_device_from_webi(step, mac):
    common.open_url('device', 'search', {'search': '%s' % mac})
    common.click_on_line_with_alert('Reset to autoprov mode', mac)
    common.open_url('device', 'search', {'search': ''})


@step(u'^When I search device "([^"]*)"$')
def when_i_search_device(step, search):
    device_manager.search_device(search)


@step(u'When I create the device with infos:')
def when_i_create_the_device_with_infos(step):
    common.open_url('device', 'add')
    device_infos = step.hashes[0]
    if 'mac' in device_infos:
        provd_cfg_dev_manager.delete_device_with_mac(device_infos['mac'])
        device_manager.type_input('mac', device_infos['mac'])
    if 'ip' in device_infos:
        provd_cfg_dev_manager.delete_device_with_ip(device_infos['ip'])
        device_manager.type_input('ip', device_infos['ip'])
    if 'plugin' in device_infos:
        device_manager.type_input('plugin', device_infos['plugin'])
    if 'template_id' in device_infos:
        device_manager.type_select('template_id', device_infos['template_id'])
    form.submit.submit_form()


@step(u'When I edit the device "([^"]*)" with infos:')
def when_i_edit_the_device_with_infos(step, device_id):
    common.open_url('device', 'edit', qry={'id': '%s' % device_id})
    device_infos = step.hashes[0]
    if 'plugin' in device_infos:
        device_manager.type_input('plugin', device_infos['plugin'])
    if 'template_id' in device_infos:
        device_manager.type_select('template_id', device_infos['template_id'])
    if 'description' in device_infos:
        device_manager.type_input('description', device_infos['description'])
    form.submit.submit_form()


@step(u'^When I delete the device "([^"]*)"$')
def when_i_delete_device(step, device_id):
    common.open_url('device', 'delete', qry={'id': '%s' % device_id})


@step(u'When I provision my device with my line_id "([^"]*)" and ip "([^"]*)"')
def when_i_provision_my_device_with_my_line_id_group1(step, line_id, device_ip):
    line = line_dao.get(line_id)
    device_helper.provision_device_using_webi(line.provisioning_extension, device_ip)


@step(u'Then the device "([^"]*)" has been provisioned with a configuration:')
def then_the_device_has_been_provisioned_with_a_configuration(step, device_id):
    provd_cfg_dev_manager.device_config_has_properties(device_id, step.hashes)


@step(u'Then I see devices with infos:')
def then_i_see_devices_with_infos(step):
    for expected_device in step.hashes:
        actual_device = device_manager.get_device_list_entry(expected_device['mac'])
        if 'ip' in expected_device:
            assert_that(actual_device['ip'], equal_to(expected_device['ip']))
        if 'configured' in expected_device:
            expected_configured = expected_device['configured'] == 'True'
            assert_that(actual_device['configured'], equal_to(expected_configured))


@step(u'Then the device "([^"]*)" has a config with the following parameters:')
def then_the_device_has_a_config_with_the_following_parameters(step, device_id):
    config = provd_cfg_dev_manager.get_provd_config(device_id)
    for expected_config in step.hashes:
        if 'vlan_enabled' in expected_config:
            assert_that(config['raw_config']['vlan_enabled'], equal_to(int(expected_config['vlan_enabled'])))


@step(u'Then the device "([^"]*)" has no config with the following keys:')
def then_the_device_group1_has_no_config_with_the_following_keys(step, device_id):
    config = provd_cfg_dev_manager.get_provd_config(device_id)
    for expected_keys in step.hashes:
        if 'vlan_enabled' in expected_keys:
            assert_that(config['raw_config'], is_not(has_key('vlan_enabled')))


@step(u'Then the device "([^"]*)" is in autoprov mode')
def then_the_device_group1_is_in_autoprov_mode(step, device_id):
    device = provd_cfg_dev_manager.get_provd_config(device_id)
    if 'config' in device:
        assert_that(device['config'], starts_with('autoprov'))


@step(u'Then I see in the log file device "([^"]*)" synchronized')
def then_i_see_in_the_log_file_device_synchronized(step, device_id):
    log_line = 'Synchronizing device %s' % device_id
    assert logs.search_str_in_daemon_log(log_line), 'No log line "%s" found in daemon.log' % log_line


@step(u'Then I see in the log file device "([^"]*)" autoprovisioned')
def then_i_see_in_the_log_file_device_group1_autoprovisioned(step, device_id):
    assert logs.search_str_in_daemon_log('Creating new config')
    assert logs.search_str_in_daemon_log('/provd/cfg_mgr/autocreate')
    assert logs.search_str_in_daemon_log('Updating device')
    assert logs.search_str_in_daemon_log('/provd/dev_mgr/devices/%s' % device_id)


@step(u'Then the device "([^"]*)" is no longer exists in provd')
def then_the_device_is_no_longer_exists_in_provd(step, device_id):
    try:
        provd_cfg_dev_manager.get_device(device_id)
    except HTTPError:
        assert True
    else:
        assert False, 'The device %s is longer exists in provd' % device_id


@step(u'Then I see in the log file device "([^"]*)" deleted')
def then_i_see_in_the_log_file_device_deleted(step, device_id):
    assert logs.search_str_in_daemon_log('Deleting device %s' % device_id)
    assert logs.search_str_in_daemon_log('/provd/dev_mgr/devices/%s' % device_id)
    assert logs.search_str_in_daemon_log('Deleting config %s' % device_id)
    assert logs.search_str_in_daemon_log('/provd/cfg_mgr/configs/%s' % device_id)
