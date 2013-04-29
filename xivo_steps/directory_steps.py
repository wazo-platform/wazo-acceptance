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

from hamcrest import assert_that, equal_to
from lettuce import step
from xivo_lettuce import assets, func
from xivo_lettuce.common import open_url, remove_element_if_exist, find_line, edit_line
from xivo_lettuce.form import submit
from xivo_lettuce.manager import directory_manager, call_manager, \
    cti_client_manager
from xivo_lettuce.manager_ws.line_manager_ws import find_line_with_extension


@step(u'Given the following directories exist:')
def given_the_following_directories_exist(step):
    for directory in step.hashes:
        remove_element_if_exist('directory_config', directory['name'])
        directory_manager.create_directory(directory)


@step(u'Given the directory definition "([^"]*)" does not exist')
def given_the_directory_definition_does_not_exist(step, definition):
    directory_manager.remove_directory(definition)


@step(u'Given the CTI directory definition is configured for LDAP searches using the ldap filter "([^"]*)"')
def given_the_cti_directory_definition_is_configured_for_ldap_searches_using_the_ldap_filter(step, ldap_filter):
    _configure_display_filter()
    _configure_ldap_directory(ldap_filter)
    _add_ldap_directory_to_direct_directories()
    _restart_cti_server(step)


def _configure_display_filter():
    field_list = [
        (u'Nom', u'', u'{db-firstname} {db-lastname}'),
        (u'Numéro', u'', u'{db-phone}')
    ]
    directory_manager.add_or_replace_display("Display", field_list)


def _configure_ldap_directory(ldap_filter):
    directory_manager.add_or_replace_directory(
        'ldapdirectory',
        'ldapfilter://%s' % ldap_filter,
        'sn,givenName,telephoneNumber',
        {'firstname': 'givenName',
        'lastname': 'sn',
        'phone': 'telephoneNumber'},
    )


def _add_ldap_directory_to_direct_directories():
    directory_manager.assign_filter_and_directories_to_context(
        'default',
        'Display',
        ['ldapdirectory']
    )


def _restart_cti_server(step):
    step.when('When I restart the CTI server')


@step(u'Given the CSV file "([^"]*)" is copied on the server into "([^"]*)"')
def given_the_csv_file_is_copied_on_the_server_into_group2(step, csvfile, serverpath):
    assets.copy_asset_to_server(csvfile, serverpath)

@step(u'Given the internal directory exists')
def given_the_internal_directory_exists(step):
    directory_manager.add_or_replace_directory(
        'internal',
        'internal',
        'userfeatures.firstname,userfeatures.lastname',
        {'firstname': 'userfeatures.firstname',
         'lastname': 'userfeatures.lastname',
         'phone': 'linefeatures.number'}
    )


@step(u'Given the internal phonebook is configured')
def given_the_internal_phonebook_is_configured(step):
    step.given('Given the internal directory exists')

    directory_manager.add_or_replace_display(
        'Display',
        [('Nom', 'name', '{db-firstname} {db-lastname}'),
         (u'Numéro', 'number_office', '{db-phone}'),
        ]
    )
    directory_manager.assign_filter_and_directories_to_context(
        'default',
        'Display',
        ['internal']
    )


@step(u'Given the directory definition "([^"]*)" is included in the default directory')
def given_the_directory_definition_group1_is_included_in_the_default_directory(step, definition):
    directory_manager.assign_filter_and_directories_to_context(
        'default',
        'Display',
        [definition]
    )


@step(u'Given extension (\d+) will answer a call and wait')
def given_extension_will_answer_a_call_and_wait(step, extension):
    line = find_line_with_extension(extension)
    call_manager.execute_sip_register(line.name, line.secret)
    time.sleep(1)
    call_manager.execute_answer_then_wait()
    time.sleep(1)


@step(u'Given extension (\d+) will answer a call, wait (\d+) seconds and hangup')
def given_extension_will_answer_a_call_wait_seconds_and_hangup(step, extension, seconds):
    line = find_line_with_extension(extension)
    call_manager.execute_sip_register(line.name, line.secret)
    time.sleep(1)
    call_manager.execute_answer_then_hangup()
    time.sleep(1)


@step(u'When I create the following directory configurations:')
def when_i_configure_the_following_directories(step):
    for directory in step.hashes:
        directory_manager.add_or_replace_directory_config(directory)


@step(u'When I edit and save the directory configuration "([^"]*)"')
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


@step(u'When I search for "([^"]*)" in the directory xlet')
def when_i_search_for_1_in_the_directory_xlet(step, search):
    cti_client_manager.set_search_for_remote_directory(search)


@step(u'When I double-click on the phone number for "([^"]*)"')
def when_i_double_click_on_the_phone_number_for_name(step, name):
    cti_client_manager.exec_double_click_on_number_for_name(name)


@step(u'Then the directory configuration "([^"]*)" has the URI "([^"]*)"')
def then_the_directory_has_the_uri(step, directory, uri):
    line = find_line(directory)
    cells = line.find_elements_by_tag_name("td")
    uri_cell = cells[2]
    assert uri_cell.text == uri


@step(u'Then nothing shows up in the directory xlet')
def then_nothing_shows_up_in_the_directory_xlet(step):
    res = cti_client_manager.get_remote_directory_infos()
    assert_that(res['return_value']['content'], equal_to([]))


@step(u'Then the following results does not show up in the directory xlet:')
def then_the_following_results_does_not_show_up_in_the_directory_xlet(step):
    res = cti_client_manager.get_remote_directory_infos()
    assert_res = func.has_subsets_of_dicts(step.hashes, res['return_value']['content'])
    assert_that(assert_res, equal_to(False))


@step(u'Then the following results show up in the directory xlet:')
def then_the_following_results_show_up_in_the_directory_xlet(step):
    res = cti_client_manager.get_remote_directory_infos()
    assert_res = func.has_subsets_of_dicts(step.hashes, res['return_value']['content'])
    assert_that(assert_res, equal_to(True))
