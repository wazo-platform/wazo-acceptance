# -*- coding: utf-8 -*-
# Copyright 2015-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import datetime
import logging
import sys
import time

from lettuce import world

from linphonelib import ExtensionNotFoundException
from linphonelib import LinphoneException
from linphonelib import Session
from linphonelib.commands import HookStatus

logger = logging.getLogger('linphone')


class CallResult(object):
    not_found = 'not_found'


class LinphoneLogWrapper(object):

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


class SipPhone(object):

    def __init__(self, config):
        if world.config['debug'].get('linphone', False):
            logfile = LinphoneLogWrapper(sys.stdout, prefix='[sip:{}]'.format(config.sip_name))
        else:
            logfile = None
        self._session = Session(config.sip_name,
                                config.sip_passwd,
                                config.sip_host,
                                config.sip_port,
                                config.rtp_port,
                                logfile)
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

    def is_ringing(self):
        return self._session.hook_status() == HookStatus.RINGING

    def is_hungup(self):
        return self._session.hook_status() == HookStatus.OFFHOOK


def register_line(sip_config):
    phone = SipPhone(sip_config)
    phone.register()
    return phone
