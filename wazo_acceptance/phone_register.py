# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class PhoneRegister:

    def __init__(self, amid_client):
        self._sip_phones = {}
        self._registered_contacts = set()
        self._amid_client = amid_client

    def find_new_sip_contact(self, endpoint):
        sections = self._amid_client.action('PJSIPShowEndpoint', {'endpoint': endpoint})
        for section in sections:
            contacts = section.get('Contacts')
            if not contacts:
                continue

            for contact in contacts.split(','):
                if contact in self._registered_contacts:
                    continue

                self._registered_contacts.add(contact)
                return 'PJSIP/{}'.format(contact)

    def add_registered_phone(self, phone, tracking_id):
        if tracking_id not in self._sip_phones:
            self._sip_phones[tracking_id] = []

        self._sip_phones[tracking_id].append(phone)

    def clear(self):
        self._sip_phones.clear()
        self._registered_contacts = set()

    def remove(self, tracking_id):
        self._sip_phones.pop(tracking_id, None)

    def get_phone(self, tracking_id, position=0):
        return self._sip_phones.get(tracking_id)[position]

    def phones(self):
        all_phones = []
        for phones in self._sip_phones.values():
            for phone in phones:
                all_phones.append(phone)
        return all_phones
