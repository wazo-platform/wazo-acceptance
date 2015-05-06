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
from hamcrest import assert_that, contains_string, is_not, has_item
from lettuce import step, world
from xivo_acceptance.action.webi import configfiles as actions
from xivo_acceptance.lettuce import common, form, logs, sysutils


@step(u'Given no config file "([^"]*)"')
def given_no_config_file_1(step, config_file_name):
    common.remove_element_if_exist('configfiles', config_file_name)


@step(u'Given there is a config file "([^"]*)"')
def given_there_is_a_config_file_group1(step, config_file_name):
    config_file_full_path = '/etc/asterisk/extensions_extra.d/%s' % config_file_name
    sysutils.send_command(['touch', config_file_full_path])
    sysutils.send_command(['echo', '[section]', '>', config_file_full_path])
    sysutils.send_command(['chown', 'asterisk:www-data', config_file_full_path])
    sysutils.send_command(['chmod', '660', config_file_full_path])


@step(u'Given I watch the log files')
def given_i_watch_the_log_files(step):
    # wait for pending actions to be written to the logs
    time.sleep(2)
    world.start_watching_log_time = sysutils.xivo_current_datetime()


@step(u'When I create a configfiles "([^"]*)" with content "([^"]*)"')
def when_i_create_configfiles_with_content(step, filename, content):
    common.open_url('configfiles', 'add')
    actions.type_file_name(filename)
    actions.type_file_content(content)
    form.submit.submit_form()


@step(u'When I create a config file "([^"]*)" without reloading dialplan')
def when_i_create_a_config_file_group1_without_reloading_dialplan(step, file_name):
    common.open_url('configfiles', 'add')
    actions.type_file_name(file_name)
    actions.type_reload_dialplan(False)
    form.submit.submit_form()


@step(u'When I create a config file "([^"]*)" and reload dialplan')
def when_i_create_a_config_file_group1_and_reload_dialplan(step, file_name):
    common.open_url('configfiles', 'add')
    actions.type_file_name(file_name)
    actions.type_reload_dialplan(True)
    form.submit.submit_form()


@step(u'When I edit the config file "([^"]*)" without reloading dialplan')
def when_i_edit_the_config_file_group1_without_reloading_dialplan(step, file_name):
    common.open_url('configfiles')
    common.edit_line(file_name)
    actions.type_reload_dialplan(False)
    form.submit.submit_form()


@step(u'When I edit the config file "([^"]*)" and reload dialplan')
def when_i_edit_the_config_file_group1_and_reload_dialplan(step, file_name):
    common.open_url('configfiles')
    common.edit_line(file_name)
    actions.type_reload_dialplan(True)
    form.submit.submit_form()


@step(u'When I import the config file "([^"]*)" and reload dialplan')
def when_i_import_the_config_file_group1_and_reload_dialplan(step, file_name):
    common.open_url('configfiles', 'import')
    actions.type_file_to_import(file_name)
    actions.type_reload_dialplan(True)
    form.submit.submit_form()


@step(u'When I import the config file "([^"]*)" without reloading dialplan')
def when_i_import_the_config_file_group1_without_reloading_dialplan(step, file_name):
    common.open_url('configfiles', 'import')
    actions.type_file_to_import(file_name)
    actions.type_reload_dialplan(False)
    form.submit.submit_form()


@step(u'When I delete the config file "([^"]*)"')
def when_i_delete_the_config_file_group1(step, file_name):
    common.open_url('configfiles')
    common.remove_line(file_name)
    # wait for dialplan to reload
    time.sleep(2)


@step(u'Then the dialplan has not been reloaded in the log files')
def then_the_dialplan_has_not_been_reloaded(step):
    def _assert():
        expected_command = 'Executing command "dialplan reload"'
        assert_that(_watched_log_lines(), is_not(has_item(contains_string(expected_command))))

    common.assert_over_time(_assert)


@step(u'Then the dialplan has been reloaded in the log files')
def then_the_dialplan_has_been_reloaded(step):
    def _assert():
        expected_command = 'Executing command "dialplan reload"'
        assert_that(_watched_log_lines(), has_item(contains_string(expected_command)))

    common.wait_until_assert(_assert, tries=3)


def _watched_log_lines():
    return logs.get_lines_since_timestamp(world.start_watching_log_time, logs.XIVO_SYSCONFD_LOG_INFO)
