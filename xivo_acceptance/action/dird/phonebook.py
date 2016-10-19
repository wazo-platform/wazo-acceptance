# -*- coding: utf-8 -*-

# Copyright (C) 2016 Proformatique
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


def create_entry(entry, phonebook_name, entity_name):
    phonebooks = world.dird_client.phonebook.list(tenant=entity_name, search=phonebook_name)['items']
    phonebook_id = [phonebook['id'] for phonebook in phonebooks if phonebook['name'] == phonebook_name][0]
    contact = {
        'firstname': entry['first name'],
        'lastname': entry['last name'],
        'displayname': entry.get('display name', '{} {}'.format(entry['first name'], entry['last name'])),
        'society': entry.get('company', ''),
        'email': entry.get('email', ''),
        'url': entry.get('website', ''),
        'number_mobile': entry.get('mobile', ''),
        'number_office': entry.get('phone', ''),
        'number_fax': entry.get('fax', ''),
        'address_office_address1': entry.get('address1', ''),
        'address_office_address2': entry.get('address2', ''),
        'address_office_city': entry.get('city', ''),
        'address_office_state': entry.get('state', ''),
        'address_office_zipcode': entry.get('zip code', ''),
        'address_office_country': entry.get('country', ''),
    }
    world.dird_client.phonebook.create_contact(contact_body=contact,
                                               phonebook_id=phonebook_id,
                                               tenant=entity_name)


def remove_entry_if_exists(entry, phonebook_name, entity_name):
    phonebooks = world.dird_client.phonebook.list(tenant=entity_name, search=phonebook_name)['items']
    phonebook_ids = [phonebook['id'] for phonebook in phonebooks if phonebook['name'] == phonebook_name]
    if not phonebook_ids:
        return
    phonebook_id = phonebook_ids[0]
    contacts = world.dird_client.phonebook.list_contacts(search=entry['first name'],
                                                         phonebook_id=phonebook_id,
                                                         tenant=entity_name)['items']
    matching_contact_ids = [contact['id'] for contact in contacts if (contact['firstname'] == entry['first name'] and
                                                                      contact['lastname'] == entry['last name'])]
    for contact_id in matching_contact_ids:
        world.dird_client.phonebook.delete_contact(contact_uuid=contact_id,
                                                   phonebook_id=phonebook_id,
                                                   tenant=entity_name)
