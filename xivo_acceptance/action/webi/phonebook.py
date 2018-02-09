# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique
# SPDX-License-Identifier: GPL-3.0+

from lettuce import world

from xivo_acceptance.lettuce import common, form


class Phonebook(object):
    def __init__(self, name, id_, entity):
        self.entity = entity
        self.name = name
        self.id = id_

    @classmethod
    def from_name(cls, phonebook_name, entity):
        token = world.config.get('auth_token')
        phonebooks = world.dird_client.phonebook.list(tenant=entity, search=phonebook_name, token=token)['items']
        phonebook_id = [phonebook['id'] for phonebook in phonebooks if phonebook['name'] == phonebook_name][0]

        return cls(phonebook_name, phonebook_id, entity)


def create_entry(entry, phonebook_name, entity):
    phonebook = Phonebook.from_name(phonebook_name, entity)

    common.open_url('phonebook', 'add_contact', {'entity': entity, 'phonebook': phonebook.id})

    display_name = _get_display_name_from_entry(entry)

    form.input.set_text_field_with_label("First Name", entry['first name'])
    form.input.set_text_field_with_label("Last Name", entry['last name'])
    form.input.set_text_field_with_label("Display name", display_name)
    form.input.set_text_field_with_label("Company", entry.get('company', ''))
    form.input.set_text_field_with_label("Mobile phone", entry.get('mobile', ''))
    form.input.set_text_field_with_label("E-mail", entry.get('email', ''))
    form.input.set_text_field_with_label("Website URL", entry.get('website', ''))

    common.go_to_tab("Office")
    form.input.set_text_field_with_label('Phone', entry.get('phone', ''))
    form.input.set_text_field_with_label('Fax', entry.get('fax', ''))
    form.input.set_text_field_with_label('Address', entry.get('address1', ''))
    form.input.set_text_field_with_label('Address (next)', entry.get('address2', ''))
    form.input.set_text_field_with_label('City', entry.get('city', ''))
    form.input.set_text_field_with_label('State', entry.get('state', ''))
    form.input.set_text_field_with_label('Zip code', entry.get('zip code', ''))
    form.select.set_select_field_with_label('Country', entry.get('country', ' '))

    form.submit.submit_form()


def _get_display_name_from_entry(entry):
    if 'display name' in entry:
        display_name = entry['display name']
    else:
        display_name = "%(first name)s %(last name)s" % entry
    return display_name


# phonebook settings
def set_accessibility_to_any_host():
    common.open_url('phonebook_settings')
    multilist = form.PhonebookSettingsMultilist.from_id('accesslist')
    multilist.remove_all()
    multilist.add('0.0.0.0/1')
    multilist.add('128.0.0.0/1')
    form.submit.submit_form()


def remove_directory_if_exists(name):
    common.remove_element_if_exist('directory_config', name, column='Name')


def create_local_dird_directory(name, phonebook_name, tenant):
    common.open_url('directory_config', 'add')

    form.input.set_text_field_with_label('Directory name', name)
    form.select.set_select_field_with_label('Type', 'Local dird phonebook')
    form.select.set_select_field_with_label('Phonebook', '{} ({})'.format(phonebook_name, tenant))

    form.submit.submit_form()
