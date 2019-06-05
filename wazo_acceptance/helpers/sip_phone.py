# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import datetime
import logging
import sys
import time

from linphonelib import (
    ExtensionNotFoundException,
    LinphoneException,
    Session,
)
from linphonelib.commands import HookStatus

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
        return '{date} {prefix} {line}'.format(date=now, prefix=self._prefix, line=line)

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
        self._call_result = None
        self.sip_port = config.sip_port
        self.rtp_port = config.rtp_port

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
        try:
            self._session.call(exten)
            self._call_result = None
        except ExtensionNotFoundException as e:
            self._call_result = e
        except LinphoneException as e:
            logger.exception(e)

    def hangup(self):
        self._session.hangup()

    def hold(self):
        self._session.hold()

    def register(self):
        self._session.register()

    def resume(self):
        self._session.resume()

    def transfer(self, exten):
        self._session.transfer(exten)

    def unregister(self):
        self._session.unregister()

    def last_call_result(self):
        if self._call_result:
            raise self._call_result

    def is_ringback_tone(self):
        return self._session.hook_status() == HookStatus.RINGBACK_TONE

    def is_talking(self):
        return self._session.hook_status() == HookStatus.ANSWERED

    def is_talking_to(self, name):
        return self._session.is_talking_to(name)

    def is_ringing(self):
        return self._session.hook_status() == HookStatus.RINGING

    def is_hungup(self):
        return self._session.hook_status() == HookStatus.OFFHOOK


class LineRegistrar:

    def __init__(self, debug):
        self._debug = debug

    def register_line(self, sip_config):
        logfile = None
        if self._debug:
            prefix = '[sip:{}]'.format(sip_config.sip_name)
            logfile = _LinphoneLogWrapper(sys.stdout, prefix=prefix)

        phone = SIPPhone(sip_config, logfile=logfile)
        phone.register()
        return phone
