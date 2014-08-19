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
from lettuce.registry import world
from selenium.webdriver.support.select import Select
from xivo_lettuce import common, form
from collections import namedtuple


FuncKeyRow = namedtuple('FuncKeyRow', ['id', 'input_type'])


FUNCKEY_DESTINATIONS = {
    'User': FuncKeyRow('user', 'autocomplete'),
    'Group': FuncKeyRow('group', 'autocomplete'),
    'Queue': FuncKeyRow('queue', 'autocomplete'),
    'Conference Room': FuncKeyRow('meetme', 'autcomplete'),
    'Customized': FuncKeyRow('custom', 'plaintext'),
    'Filtering Boss - Secretary': FuncKeyRow('extenfeatures-bsfilter', 'dropdown'),
    'Enable / Disable forwarding on no answer': FuncKeyRow('extension', 'plaintext'),
    'Enable / Disable forwarding on busy': FuncKeyRow('extension', 'plaintext'),
    'Enable / Disable forwarding unconditional': FuncKeyRow('extension', 'plaintext'),
    'Connect/Disconnect an agent': FuncKeyRow('extenfeatures-agentstaticlogtoggle', 'autocomplete'),
    'Connect an agent': FuncKeyRow('extenfeatures-agentstaticlogin', 'autocomplete'),
    'Disconnect an agent': FuncKeyRow('extenfeatures-agentstaticlogoff', 'autocomplete'),
    'Parking': FuncKeyRow('extension', 'plaintext'),
    'Parking Position': FuncKeyRow('extension', 'plaintext'),
    'Paging': FuncKeyRow('extension', 'plaintext'),
}


def type_user_names(firstName, lastName):
    world.browser.find_element_by_id('it-userfeatures-firstname', 'User form not loaded')
    input_firstName = world.browser.find_element_by_id('it-userfeatures-firstname')
    input_lastName = world.browser.find_element_by_id('it-userfeatures-lastname')
    input_firstName.clear()
    input_firstName.send_keys(firstName)
    input_lastName.clear()
    input_lastName.send_keys(lastName)


def find_func_key_line(number=None):
    if number:
        number = str(number)
    else:
        number = 'last()'

    xpath = "//tbody[@id='phonefunckey']/tr[%s]" % number
    return world.browser.find_element_by_xpath(xpath)


def find_key_number_field(line):
    return Select(line.find_element_by_name('phonefunckey[fknum][]'))


def find_key_type_field(line):
    return Select(line.find_element_by_name('phonefunckey[type][]'))


def find_key_label_field(line):
    return line.find_element_by_name('phonefunckey[label][]')


def find_key_supervision_field(line):
    return Select(line.find_element_by_name('phonefunckey[supervision][]'))


def add_funckey_line():
    add_button = world.browser.find_element_by_xpath("//div[@id='sb-part-funckeys']//a[@id='add_funckey_button']")
    add_button.click()


def get_line_number(line):
    element = line.find_element_by_name('phonefunckey[type][]')
    _, _, line_number = element.get_attribute('id').rpartition('-')
    return int(line_number)


def find_key_destination_field(key_type, line):
    destination = FUNCKEY_DESTINATIONS[key_type]

    line_number = get_line_number(line)
    if destination.input_type in ('plaintext', 'dropdown'):
        field_id = "it-phonefunckey-%s-typeval-%s" % (destination.id, line_number)
    elif destination.input_type == 'autocomplete':
        field_id = "it-phonefunckey-%s-suggest-%s" % (destination.id, line_number)
    return line.find_element_by_id(field_id)


def type_func_key(key_type, destination, key_number=None, label=None, supervised=None):
    common.go_to_tab('Func Keys')

    add_funckey_line()

    current_line = find_func_key_line()

    key_type_field = find_key_type_field(current_line)
    key_type_field.select_by_visible_text(key_type)

    _fill_destination_field(key_type, current_line, destination)

    if key_number:
        key_number_field = find_key_number_field(current_line)
        key_number_field.select_by_visible_text(key_number)

    if label:
        label_field = find_key_label_field(current_line)
        label_field.send_keys(label)

    if supervised:
        supervision_field = find_key_supervision_field(current_line)
        supervision_field.select_by_visible_text(supervised)


def _fill_destination_field(key_type, line, destination):
    field = find_key_destination_field(key_type, line)
    destination_row = FUNCKEY_DESTINATIONS[key_type]

    if destination_row.input_type == 'plaintext':
        field.send_keys(destination)
    elif destination_row.input_type == 'dropdown':
        Select(field).select_by_visible_text(destination)
    elif destination_row.input_type == 'autocomplete':
        field.send_keys(destination)
        field_id = "__dwho-suggest__%s-res-1" % destination.id
        autocomplete_element = line.find_element_by_id(field_id)
        autocomplete_element.click()


def change_key_order(pairs):
    common.go_to_tab('Func Keys')
    for old, new in pairs:
        current_line = world.browser.find_element_by_xpath('''//tbody[@id='phonefunckey']/tr[%s]''' % old)
        number_field = Select(current_line.find_element_by_name('phonefunckey[fknum][]'))
        number_field.select_by_visible_text(new)


def user_form_add_line(linenumber, context='default', protocol='SIP', device=None, entity_displayname=None):
    open_line_tab()
    if entity_displayname is not None:
        select_entity_with_displayname(entity_displayname)
    click_add_line_button()
    select_context(context)
    type_line_number(linenumber)
    select_protocol(protocol)
    if device is not None:
        select_device(device)
    common.go_to_tab('General')


def open_line_tab():
    common.go_to_tab('Lines')


def click_add_line_button():
    add_button = world.browser.find_element_by_id('lnk-add-row')
    add_button.click()


def select_entity_with_displayname(entity_displayname):
    input_entity = world.browser.find_elements_by_id('it-userfeatures-entityid')[0]
    Select(input_entity).select_by_visible_text(entity_displayname)


def select_context(context):
    input_context = world.browser.find_elements_by_id('linefeatures-context')[-2]
    Select(input_context).select_by_value(context.lower())


def type_line_number(linenumber):
    input_linenumber = world.browser.find_elements_by_id('linefeatures-number')[-2]
    input_linenumber.send_keys(linenumber)


def select_protocol(protocol):
    input_protocol = Select(world.browser.find_elements_by_id('linefeatures-protocol')[-2])
    input_protocol.select_by_visible_text(protocol)


def type_device(device):
    open_line_tab()
    select_device(device)


def select_device(device):
    input_device_1 = world.browser.find_element_by_xpath('//a[@class="select2-choice"]')
    input_device_1.click()
    input_device_2 = world.browser.find_element_by_xpath('//input[contains(@class, "select2-input")]')
    input_device_2.send_keys(device)
    input_device_3 = world.browser.find_element_by_xpath('//li[contains(@class, "select2-result")]',
                                                         'No device %s found' % device)
    input_device_3.click()


def type_voicemail(voicemail_number):
    common.go_to_tab('General')
    form.select.set_select_field_with_label('Language', 'en_US')
    common.go_to_tab('Voicemail')
    form.select.set_select_field_with_label('Voice Mail', 'Asterisk')
    form.input.set_text_field_with_label('Voicemail', voicemail_number)


def type_mobile_number(mobile_number):
    common.go_to_tab('General')
    form.input.set_text_field_with_label('Mobile phone number', mobile_number)


def remove_line():
    common.go_to_tab('Lines')
    select_line = world.browser.find_element_by_xpath("//table[@id='list_linefeatures']/tbody/tr//input[@id='linefeatures-number']")
    delete_button = select_line.find_element_by_xpath("//a[@title='Delete this line']")
    delete_button.click()
    time.sleep(world.timeout)


def switchboard_config_for_user(user):
    common.open_url('user')
    common.edit_line(user)
    select_simultaneous_calls(1)
    enable_call_transfer()
    form.submit.submit_form()


def select_simultaneous_calls(nb_calls):
    form.select.set_select_field_with_id("it-userfeatures-simultcalls", str(nb_calls))


def enable_call_transfer():
    common.go_to_tab("Services")
    form.checkbox.check_checkbox_with_id("it-userfeatures-enablehint")


def get_user_list_entry(search_fullname):
    user_tr = common.get_line(search_fullname)
    fullname = user_tr.find_element_by_class_name('col_fullname').text
    provisioning_code = user_tr.find_element_by_class_name('col_provisioning_code').text
    number = user_tr.find_element_by_class_name('col_number').text
    protocol = user_tr.find_element_by_class_name('col_protocol').text
    return {
        'fullname': fullname,
        'provisioning_code': provisioning_code,
        'number': number,
        'protocol': protocol
    }


def deactivate_bsfilter(user):
    common.open_url('user', 'search', {'search': user})
    common.edit_line(user)
    common.go_to_tab('Services')
    form.select.set_select_field_with_id('it-userfeatures-bsfilter', 'No')
    form.submit.submit_form()


def get_chantype_of_group(group_name):
    chantype_select = _get_chantype_select_of_group(group_name)
    return chantype_select.first_selected_option.text


def select_chantype_of_group(group_name, text):
    chantype_select = _get_chantype_select_of_group(group_name)
    chantype_select.select_by_visible_text(text)


def _get_chantype_select_of_group(group_name):
    common.go_to_tab('Groups')
    select_name = 'group[%s][chantype]' % group_name
    select_element = world.browser.find_element_by_name(select_name)
    return Select(select_element)
