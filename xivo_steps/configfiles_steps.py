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

from hamcrest import assert_that, contains_string, is_not, has_item
from lettuce import step, world
from xivo_lettuce import common, form, logs
from xivo_lettuce.form.checkbox import Checkbox


@step(u'Given no config file "([^"]*)"')
def given_no_config_file_1(step, config_file_name):
    common.remove_element_if_exist('configfiles', config_file_name)


@step(u'When I create a configfiles "([^"]*)" with content "([^"]*)"')
def when_i_create_configfiles_with_content(step, filename, content):
    common.open_url('configfiles', 'add')
    input_filename = world.browser.find_element_by_id('it-configfile-filename')
    input_filename.clear()
    input_filename.send_keys(filename)
    input_description = world.browser.find_element_by_id('it-configfile-description')
    input_description.clear()
    input_description.send_keys(content)
    form.submit.submit_form()


@step(u'When I create a config file "([^"]*)" without reloading dialplan')
def when_i_create_a_config_file_group1_without_reloading_dialplan(step, file_name):
    common.open_url('configfiles', 'add')
    input_filename = world.browser.find_element_by_id('it-configfile-filename')
    input_filename.clear()
    input_filename.send_keys(file_name)
    input_reload_dialplan = Checkbox(world.browser.find_element_by_id('it-configfile-reload-dialplan'))
    input_reload_dialplan.uncheck()
    form.submit.submit_form()


@step(u'When I create a config file "([^"]*)" and reload dialplan')
def when_i_create_a_config_file_group1_and_reload_dialplan(step, file_name):
    common.open_url('configfiles', 'add')
    input_filename = world.browser.find_element_by_id('it-configfile-filename')
    input_filename.clear()
    input_filename.send_keys(file_name)
    input_reload_dialplan = Checkbox(world.browser.find_element_by_id('it-configfile-reload-dialplan'))
    input_reload_dialplan.check()
    form.submit.submit_form()


@step(u'When I edit the config file "([^"]*)" without reloading dialplan')
def when_i_edit_the_config_file_group1_without_reloading_dialplan(step, file_name):
    common.open_url('configfiles')
    common.edit_line(file_name)
    input_reload_dialplan = Checkbox(world.browser.find_element_by_id('it-configfile-reload-dialplan'))
    input_reload_dialplan.uncheck()
    form.submit.submit_form()


@step(u'When I edit the config file "([^"]*)" and reload dialplan')
def when_i_edit_the_config_file_group1_and_reload_dialplan(step, file_name):
    common.open_url('configfiles')
    common.edit_line(file_name)
    input_reload_dialplan = Checkbox(world.browser.find_element_by_id('it-configfile-reload-dialplan'))
    input_reload_dialplan.check()
    form.submit.submit_form()


@step(u'Then the dialplan has not been reloaded')
def then_the_dialplan_has_not_been_reloaded(step):
    expected_command = "Asterisk command 'dialplan reload' successfully executed"
    log_lines = logs.find_line_in_daemon_log()
    assert_that(log_lines, is_not(has_item(contains_string(expected_command))))


@step(u'Then the dialplan has been reloaded')
def then_the_dialplan_has_been_reloaded(step):
    expected_command = "Asterisk command 'dialplan reload' successfully executed"
    log_lines = logs.find_line_in_daemon_log()
    assert_that(log_lines, has_item(contains_string(expected_command)))
