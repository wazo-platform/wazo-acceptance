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

from lettuce import world

from xivo_lettuce import form
from xivo_lettuce.common import remove_element_if_exist, open_url, \
    go_to_tab


def phonebook_search(term):
    open_url('phonebook')
    form.input.set_text_field_with_id("it-toolbar-search", term)
    form.submit.submit_form("it-subsearch")


def create_entry(entry):
    open_url('phonebook', 'add')

    display_name = _get_display_name_from_entry(entry)

    form.input.set_text_field_with_label("First Name", entry['first name'])
    form.input.set_text_field_with_label("Last Name", entry['last name'])
    form.input.set_text_field_with_label("Display name", display_name)

    go_to_tab("Office")
    form.input.set_text_field_with_label('Phone', entry.get('phone', ''))

    form.submit.submit_form()


def remove_entry_if_exists(entry):
    display_name = _get_display_name_from_entry(entry)
    remove_entry_matching(display_name)


def _get_display_name_from_entry(entry):
    if 'display name' in entry:
        display_name = entry['display name']
    else:
        display_name = "%(first name)s %(last name)s" % entry
    return display_name


def remove_entry_matching(search):
    phonebook_search(search)
    remove_element_if_exist("phonebook", search)
    phonebook_search('')


def import_csv_file(path):
    open_url('phonebook', 'import')
    element = world.browser.find_element_by_id("it-import")
    element.send_keys(path)
    form.submit.submit_form()


# phonebook settings
def set_accessibility_to_any_host():
    open_url('phonebook_settings')
    multilist = form.PhonebookSettingsMultilist.from_id('accesslist')
    multilist.remove_all()
    multilist.add('0.0.0.0/1')
    multilist.add('128.0.0.0/1')
    form.submit.submit_form()
