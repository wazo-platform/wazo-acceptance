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

import time

from lettuce import step, world
from xivo_lettuce import assets
from xivo_lettuce.common import open_url, remove_element_if_exist, find_line, edit_line
from xivo_lettuce.form import submit
from xivo_lettuce.manager import directory_manager
from xivo_lettuce.xivoclient import xivoclient_step


@step(u'Given the directory "([^"]*)" does not exist')
def given_the_directory_does_not_exist(step, directory):
    remove_element_if_exist('directory_config', directory)


@step(u'Given the following directories exist:')
def given_the_following_directories_exist(step):
    for directory in step.hashes:
        remove_element_if_exist('directory_config', directory['name'])
        directory_manager.create_directory(directory)


@step(u'Given the directory definition "([^"]*)" does not exist')
def given_the_directory_definition_does_not_exist(step, definition):
    remove_element_if_exist('cti_directory', 'phonebookcsv')
    #Work around for directory associations that aren't deleted
    open_url('cti_direct_directory', 'list')
    try:
        edit_line('default')
    except Exception:
        pass  # No default context configured
    else:
        submit.submit_form()


@step(u'Given the CSV file "([^"]*)" is copied on the server into "([^"]*)"')
def given_the_csv_file_is_copied_on_the_server_into_group2(step, csvfile, serverpath):
    assets.copy_asset_to_server(csvfile, serverpath)


@step(u'When I configure the following directories:')
def when_i_configure_the_following_directories(step):
    for directory in step.hashes:
        directory_manager.create_directory(directory)


@step(u'Then the directory "([^"]*)" has the URI "([^"]*)"')
def then_the_directory_has_the_uri(step, directory, uri):
    line = find_line(directory)
    cells = line.find_elements_by_tag_name("td")
    uri_cell = cells[2]
    assert uri_cell.text == uri


@step(u'When I edit and save the directory "([^"]*)"')
def when_i_edit_and_save_the_directory(step, directory):
    open_url('directory_config', 'list')
    edit_line(directory)
    submit.submit_form()


@step(u'When I add the following CTI directory definition:')
def when_i_add_the_following_cti_directory_definition(step):
    for directory in step.hashes:
        directory_manager.add_directory_definition(directory)


@step(u'When I map the following fields and save the directory definition:')
def when_i_map_the_following_fields_and_save_the_directory_definition(step):
    for field in step.hashes:
        directory_manager.add_field(field['field name'], field['value'])
    submit.submit_form()


@step(u'When I include "([^"]*)" in the default directory')
def when_i_include_phonebook_in_the_default_directory(step, phonebook):
    directory_manager.assign_filter_and_directories_to_context(
        'default',
        'Display',
        [phonebook]
    )


@step(u'When I restart the CTI server')
def when_i_restart_the_cti_server(step):
    command = ["/etc/init.d/xivo-ctid", "restart"]
    world.ssh_client_xivo.check_call(command)
    time.sleep(10)


@step(u'When I search for "([^"]*)" in the directory xlet')
@xivoclient_step
def when_i_search_for_1_in_the_directory_xlet(step, search):
    assert world.xc_response == 'OK'


@step(u'Then nothing shows up in the directory xlet')
@xivoclient_step
def then_nothing_shows_up_in_the_directory_xlet(step):
    assert world.xc_response == 'OK'


@step(u'Then "([^"]*)" shows up in the directory xlet')
@xivoclient_step
def then_1_shows_up_in_the_directory_xlet(step, entry):
    assert world.xc_response == 'OK'
