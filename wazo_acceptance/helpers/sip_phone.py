# Copyright 2015-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import datetime
import logging
import sys
import time

from linphonelib import LinphoneException, Session
from linphonelib.commands import CallStatus, RegisterStatus

logger = logging.getLogger('linphone')


class _LinphoneLogWrapper:

    def __init__(self, file_, prefix):
        self._file = file_
        self._prefix = prefix

    def write(self, data):
        data = self._prefix_lines(data)
        data = self._add_last_newline(data)
        return self._file.write(data)

    def __getattr__(self, attr):
        return getattr(self._file, attr)

    def _prefix_lines(self, data):
        lines = data.split('\n')
        prefixed_lines = [self._prefix_line(line) for line in lines]
        return '\n'.join(prefixed_lines)

    def _prefix_line(self, line):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        return f'{now} {self._prefix} {line}'

    def _add_last_newline(self, data):
        if not data.endswith('\n'):
            return data + '\n'
        return data


class SIPPhone:

    def __init__(self, config, logfile=None):
        self._session = Session(
            config.sip_name,
            config.sip_passwd,
            config.sip_host,
            config.sip_port,
            config.rtp_port,
            logfile,
        )
        self._name = config.sip_name
        self.sip_port = config.sip_port
        self.rtp_port = config.rtp_port

    def disconnect(self):
        self._session.close()

    def answer(self, timeout=5):
        start = time.time()
        exception = None
        while time.time() - start < timeout:
            try:
                self._session.answer()
            except LinphoneException as e:
                exception = e
            else:
                return
        if exception:
            raise exception

    def call(self, exten):
        self._session.call(exten)

    def hangup(self):
        self._session.hangup()

    def hold(self):
        self._session.hold()

    def register(self):
        self._session.register()

    def resume(self):
        self._session.resume()

    def send_dtmf(self, digit):
        self._session.send_dtmf(digit)
        # NOTE(fblackburn): linphone DTMF length is 100ms
        time.sleep(0.150)

    def transfer(self, exten):
        self._session.transfer(exten)

    def unregister(self):
        self._session.unregister()

    def is_talking(self):
        return self._session.call_status() == CallStatus.ANSWERED

    def is_talking_to(self, name):
        return self._session.is_talking_to(name)

    def is_ringing(self):
        return self._session.call_status() == CallStatus.RINGING

    def is_ringing_showing(self, name):
        return self._session.is_ringing_showing(name)

    def is_hungup(self):
        return self._session.call_status() == CallStatus.OFF

    def is_registered(self):
        return self._session.register_status() == RegisterStatus.REGISTERED

    def is_holding(self, context):
        response = context.amid_client.action('DeviceStateList')
        device_name = f'PJSIP/{self._name}'
        return any(device.get('Device') == device_name and device.get('State') == 'ONHOLD'
                   for device in response)

    @property
    def sip_username(self):
        return self._name


class PhoneFactory:

    def __init__(self, context, debug):
        self._context = context
        self._debug = debug

    def _register_line(self, sip_config):
        logfile = None
        if self._debug:
            prefix = f'[sip:{sip_config.sip_name}]'
            logfile = _LinphoneLogWrapper(sys.stdout, prefix=prefix)

        phone = SIPPhone(sip_config, logfile=logfile)
        try:
            phone.register()
        except LinphoneException:
            phone.disconnect()
            raise

        return phone

    def register_and_track_phone(self, tracking_id, endpoint_sip):
        phone_config = self._context.helpers.sip_config.create(endpoint_sip)
        phone = self._register_line(phone_config)
        name = endpoint_sip['name']
        phone.sip_contact_uri = self._context.phone_register.find_new_sip_contact(name)
        self._context.phone_register.add_registered_phone(phone, tracking_id)
        return phone
