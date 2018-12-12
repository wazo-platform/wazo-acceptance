# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+


class PhoneRegister(object):

    def __init__(self):
        self._sip_phones = {}

    def add_registered_phone(self, phone, name):
        if name not in self._sip_phones:
            self._sip_phones[name] = []

        self._sip_phones[name].append(phone)

    def clear(self):
        self._sip_phones.clear()

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
