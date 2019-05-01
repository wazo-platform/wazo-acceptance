# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import world


class PhoneRegister(object):

    def __init__(self):
        self._sip_phones = {}
        self._registered_contacts = set()

    def find_new_sip_contact(self, endpoint):
        sections = world.amid_client.action('PJSIPShowEndpoint', {'endpoint': endpoint})
        for section in sections:
            contacts = section.get('Contacts')
            if not contacts:
                continue

            for contact in contacts.split(','):
                if contact in self._registered_contacts:
                    continue

                self._registered_contacts.add(contact)
                return 'PJSIP/{}'.format(contact)

    def add_registered_phone(self, phone, name):
        if name not in self._sip_phones:
            self._sip_phones[name] = []

        self._sip_phones[name].append(phone)

    def clear(self):
        self._sip_phones.clear()
        self._registered_contacts = set()

    def remove(self, name):
        self._sip_phones.pop(name, None)

    def get_user_phone(self, name, position=0):
        return self._sip_phones.get(name)[position]

    def phones(self):
        all_phones = []
        for phones in self._sip_phones.itervalues():
            for phone in phones:
                all_phones.append(phone)
        return all_phones
