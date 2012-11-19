# -*- coding: utf-8 -*-
import time

from lettuce import step, world
from selenium.webdriver.support.select import Select
from xivo_lettuce import assets
from xivo_lettuce.common import open_url, remove_element_if_exist, find_line, edit_line
from xivo_lettuce.form import submit
from xivo_lettuce.manager import directory_manager
from xivo_lettuce.xivoclient import xivoclient_step

@step(u'Given the directory "([^"]*)" does not exist')
def given_the_directory_does_not_exist(step, directory):
    remove_element_if_exist('directory_config', directory)


@step(u'Given the directory definition "([^"]*)" does not exist')
def given_the_directory_definition_does_not_exist(step, definition):
    remove_element_if_exist('cti_directory', 'phonebookcsv')
    #Work around for directory assocations that
    #aren't deleted 
    open_url('cti_direct_directory', 'list')
    edit_line('default')
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
    open_url('cti_direct_directory', 'list')
    edit_line('default')
    directory_manager.add_directory_to_context(phonebook)
    submit.submit_form()


@step(u'When I restart the CTI server')
def when_i_restart_the_cti_server(step):
    command = ["/etc/init.d/xivo-ctid", "restart"]
    world.ssh_client_xivo.check_call(command)
    time.sleep(10)


@step(u'Then "([^"]*)" shows up in the directory xlet after searching for "([^"]*)"')
@xivoclient_step
def then_user_shows_up_in_the_directory_xlet_after_searching(step, user, search):
    assert world.xc_response == 'OK'

