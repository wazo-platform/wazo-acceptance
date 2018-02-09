# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Avencall
# SPDX-License-Identifier: GPL-3.0+


class PhoneRegister(object):

    def __init__(self):
        self._sip_phones = {}

    def add_registered_phone(self, phone, name):
        self._sip_phones[name] = phone

    def clear(self):
        self._sip_phones.clear()

    def remove(self, name):
        self._sip_phones.pop(name, None)

    def get_user_phone(self, name):
        return self._sip_phones.get(name)

    def phones(self):
        return self._sip_phones
